from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from login.models import Bar, Twitter

import login.secrets as secrets
import login.matching_libraries as match

import urllib.request, json
import requests
from requests.auth import HTTPBasicAuth

import pprint
import datetime
import tweepy
from string import ascii_letters, digits

consumer_key = secrets.consumer_key
consumer_secret = secrets.consumer_secret
access_token = secrets.access_token
access_secret = secrets.access_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

API = tweepy.API(auth)

def home_page(request):
	if request.method == 'POST':
		return render_after_POST(request)

	else:
		return render_default_home_page(request)

def render_default_home_page(request):
	return render(request, 'home.html', {
		'new_location_text': '45.5200165, -122.67926349999999',
		'zoom': 13
		})

def render_after_POST(request):
	coordinates = get_google_coordinates(request)
	bars = get_google_bars(coordinates)
	current_bars_list = bars_to_class(bars)
	check_database_for_bar(current_bars_list)
	marker_coordinates = draw_markers(current_bars_list, request)


	return render(request, 'home.html', {
		'new_location_text': coordinates,
		'zoom': 15,
		'markers': marker_coordinates
		})

def get_google_coordinates(request):
	key = '&key='+ secrets.googlekey
	search_text = request.POST.get('location_text', '').replace(' ', '+')

	Loc_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
	googleResponseLoc = urllib.request.urlopen(Loc_URL+search_text+key)
	str_responseLoc = googleResponseLoc.read().decode('utf-8') #convert googleResponse to be readable
	jsonResponseLoc = json.loads(str_responseLoc)

	latitude = str(jsonResponseLoc['results'][0]['geometry']['location']['lat'])
	longitude = str(jsonResponseLoc['results'][0]['geometry']['location']['lng'])
	# latitude = str(45.5164111) # hard coded latitude and longitude used to limit API calls
	# longitude = str(-122.6156611)
	coordinates = latitude + ',' + longitude
	return coordinates

def get_google_bars(coordinates):
	nearby_URL1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
	nearby_URL2 = '&radius=600&types=bar&key='
	key = secrets.googlekey

	googleResponseBars = urllib.request.urlopen(nearby_URL1+coordinates+nearby_URL2+key)
	str_responseBars = googleResponseBars.read().decode('utf-8')
	jsonResponseBars = json.loads(str_responseBars)
	return jsonResponseBars


def bars_to_class(bars):
	current_bars = [CurrentBar(bar) for bar in bars['results']] 
	# current_bars = [CurrentBar(bars['results'][1])] #USED TO LIMIT BARS RETURNED TO 1
	return current_bars

class CurrentBar():
	def __init__(self, bar):
		self.google_id = bar['id']
		self.name = bar['name']
		self.stripped_name = extract_alphanumeric(bar['name'].lower())
		self.latitude = bar['geometry']['location']['lat']
		self.longitude = bar['geometry']['location']['lng']
		if 'vicinity' in bar:
			self.vicinity = bar['vicinity']
		if 'price_level' in bar:
			self.price_level = bar['price_level']
		if 'rating' in bar:
			self.rating = bar['rating']
		self.accessed_date = timezone.now()
		if 'opening_hours' in bar and 'open_now' in bar['opening_hours']:
			self.open_at_update = bar['opening_hours']['open_now']

def extract_alphanumeric(string):
    return "".join([char for char in string if char in (ascii_letters + digits)])



def check_database_for_bar(current_bars):
	for current_bar in current_bars:
		if Bar.objects.filter(google_id=current_bar.google_id):
			# compare_date_time()
			update_bar_in_db(current_bar)
			# update_tweets_in_db(current_bar)
		else:
			create_bar_in_db(current_bar)

			twitter_name = bing_search(current_bar)
			twitter = API.user_timeline(screen_name=twitter_name, count=2)
			if twitter and verify_twitter(twitter):
				create_twitter_in_db(current_bar.google_id, twitter)
				save_twitter_attributes(current_bar.google_id, twitter)

def save_twitter_attributes(current_bar_id, twitter):
	t = Twitter.objects.get(google_id=current_bar_id)
	attributes = []
	for k, v in match.ATTRIBUTE_REGISTRY.items():
		for item in v:
			if item in t.statuses.lower():
				attributes.append(k)
	if attributes:
		t.tweet_attributes = attributes
		t.save()
	
				
def create_twitter_in_db(current_bar_id, twitter):
	tweets = []
	for status in twitter:
		tweets.append(status.text)
	t = Twitter()
	t.google_id = current_bar_id
	t.screen_name = twitter[0].user.screen_name
	t.created_at = twitter[0].user.created_at
	try:
		t.location = twitter[0].user.location
	except:
		pass
	try:
		t.profile_image = twitter[0].user.profile_image_url_https
	except:
		pass
	try:
		t.profile_banner = twitter[0].user.profile_banner_url
	except:
		pass
	try:
		t.profile_link_color = twitter[0].user.profile_link_color
	except:
		pass
	try:
		t.website = twitter[0].user.entities['url']['urls'][0]['expanded_url']
	except:
		pass
	t.updated_date = timezone.now()	
	if tweets:
		t.statuses = tweets
	t.save()

# def create_tweets_in_db(twitter_info, current_bar):


# 			if twitter:
# 				twitter_info = API.user_timeline(screen_name=twitter.screen_name)

def create_bar_in_db(current_bar):
	b = Bar()
	b.google_id = current_bar.google_id
	b.name = current_bar.name
	b.stripped_name = current_bar.stripped_name
	b.latitude = current_bar.latitude
	b.longitude = current_bar.longitude
	if hasattr(current_bar, 'vicinity'):
		b.vicinity = current_bar.vicinity
	if hasattr(current_bar, 'price_level'):
		b.price_level = current_bar.price_level
	if hasattr(current_bar, 'rating'):
		b.rating = current_bar.rating
	b.creation_date = timezone.now()
	if hasattr(current_bar, 'open_at_update'):
		b.open_at_update = current_bar.open_at_update
	b.save()


def update_bar_in_db(current_bar):
	b = Bar.objects.get(google_id=current_bar.google_id)
	if hasattr(current_bar, 'vicinity'):
		b.vicinity = current_bar.vicinity
	if hasattr(current_bar, 'price_level'):
		b.price_level = current_bar.price_level
	if hasattr(current_bar, 'rating'):
		b.rating = current_bar.rating
	b.updated_date = timezone.now()
	if hasattr(current_bar, 'open_at_update'):
		b.open_at_update = current_bar.open_at_update
	b.save()

def bing_search(current_bar):

	API_KEY = 'q0D7TMvQsCC3x+s8+QdD++9OK+3eUN4QuodsL3oK6Sc'
	user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
	headers= {'User-Agent': user_agent}
	auth = HTTPBasicAuth(API_KEY, API_KEY)

	URL1 = "https://api.datamarket.azure.com/Bing/Search/v1/Web?Query=%27"
	query = (extract_alphanumeric_whitespace(current_bar.name)).replace(' ', '%20')
	URL2 = "%20Portland%20site%3Atwitter.com%27&$top=1&$format=json"
	url = URL1 + query + URL2

	response_data = requests.get(url, headers=headers, auth=auth)
	bing_result = response_data.json()
	if bing_result['d']['results']:
		return bing_result['d']['results'][0]['Url'].rsplit('/', 1)[-1].lower()

def extract_alphanumeric_whitespace(string):
    return "".join([char for char in string if char in (ascii_letters + digits + ' ')])

def draw_markers(current_bars_list, request):
	markers = []
	red = 'https://storage.googleapis.com/support-kms-prod/SNP_2752125_en_v0'
	green = 'https://storage.googleapis.com/support-kms-prod/SNP_2752129_en_v0'
	yellow = 'https://storage.googleapis.com/support-kms-prod/SNP_2752063_en_v0'
	input_ids = request.POST.getlist('inputs')
	print(input_ids)
	for bar in current_bars_list:
		b = Bar.objects.get(google_id=bar.google_id)
		try: 
			t = Twitter.objects.get(google_id=bar.google_id)
			truth = False
			for item in input_ids:
				if item in t.tweet_attributes:
					markers.append([b.latitude, b.longitude, '/static/'+item+'.png'])
					truth = True
					break
			if truth == False:
				markers.append([b.latitude, b.longitude, green])
		except:
			markers.append([b.latitude, b.longitude, red])
	return markers


	# for x in current_bars_list:
	# 	q = Bar.objects.get(google_id=x.google_id)



		# try:
		# 	t = Twitter.objects.get(google_id=x.google_id)
		# except:
		# 	t = None
		# if t:
		# 	if t.tweet_attributes:
		# 		marker_coordinates = [q.latitude, q.longitude, green]
		# 	else:
		# 		marker_coordinates = [q.latitude, q.longitude, yellow]
		# else:
		# 	marker_coordinates = [q.latitude, q.longitude, red]
		# markers.append(marker)
	# return markers


def verify_twitter(twitter_info):
	if any(location in twitter_info[0].user.location for location in match.location):
		return True
	else:
		return False





# 2661f5

# def get_twitter_statuses(matched_twitters):
# 	for item in matched_twitters:
# 		status = API.user_timeline(screen_name=item.name, count=2)
# 		pprint.pprint(vars(status[0]))
# 		#user
# 		created_at = status[0].user.created_at
# 		screen_name = status[0].user.screen_name
# 		name = status[0].user.name
# 		profile_image = status[0].user.profile_image_url_https  #_bigger
# 		profile_banner = status[0].user.profile_banner_url #300x100
# 		profile_link_color = status[0].user.profile_link_color 
# 		profile_sidebar_border_color = status[0].user.profile_sidebar_border_color
# 		display_url = status[0].user.entities['url']['urls'][0]['display_url']
# 		expaned_url = status[0].user.entities['url']['urls'][0]['expanded_url']
# 		location = status[0].user.location

# 		#statuses
# 		created_at = status[0].created_at
# 		text = status[0].text
# 		url1 = status[0].entities['urls'][0]['expanded_url']
		# extended_entities = status[0].extended_entities['media'][0]['display_url']


