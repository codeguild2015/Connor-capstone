from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from login.models import Bar, Twitter

import login.secrets as secrets
import login.matching_libraries as match

import urllib.request, json
import requests
from requests.auth import HTTPBasicAuth
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
	""" When a request comes into the home page, route it based on if its a post request"""
	if request.method == 'POST':
		return render_after_POST(request)

	else:
		return render_default_home_page(request)


def render_default_home_page(request):
	""" Renders the default home page with a preset map center and zoom level """
	return render(request, 'home.html', {
		'new_location_text': '45.5200165, -122.67926349999999',
		'zoom': 13
		})


def render_after_POST(request):
	""" Calls the google functions, and renders the home page with map markers added to the map """
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
	""" Takes in an address sent via post, and makes a google API geocode call on it to retrieve and return 
	the latitude and longitude of that address 
	"""
	key = '&key='+ secrets.googlekey
	search_text = request.POST.get('location_text', '').replace(' ', '+')

	Loc_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
	googleResponseLoc = urllib.request.urlopen(Loc_URL+search_text+key)
	str_responseLoc = googleResponseLoc.read().decode('utf-8') #convert googleResponse to be readable
	jsonResponseLoc = json.loads(str_responseLoc)

	latitude = str(jsonResponseLoc['results'][0]['geometry']['location']['lat'])
	longitude = str(jsonResponseLoc['results'][0]['geometry']['location']['lng'])
	coordinates = latitude + ',' + longitude
	return coordinates


def get_google_bars(coordinates):
	""" Takes in latitude and logitude coordinates, makes a google API nearbysearch call for bars 
	located within 600 meters of those coordinates, and returns a list of the bars in the form of a 
	json response
	 """
	nearby_URL1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
	nearby_URL2 = '&radius=600&types=bar&key='
	key = secrets.googlekey

	googleResponseBars = urllib.request.urlopen(nearby_URL1+coordinates+nearby_URL2+key)
	str_responseBars = googleResponseBars.read().decode('utf-8')
	jsonResponseBars = json.loads(str_responseBars)
	return jsonResponseBars


def bars_to_class(bars):
	""" Takes in a list of bars in json format, and returns a list of bar Objects created using the
	CurrentBar() class
	"""
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
	""" takes in a string and returns the string with all non-alphanumeric characters removed  """
    return "".join([char for char in string if char in (ascii_letters + digits)])


def check_database_for_bar(current_bars):
	""" main database function. takes in a list of current bars, and checks if it exists in the database.

	"""
	for current_bar in current_bars:
		if Bar.objects.filter(google_id=current_bar.google_id):
			# compare_date_time() MAKE
			update_bar_in_db(current_bar)
			# update_tweets_in_db(current_bar) MAKE
		else:
			create_bar_in_db(current_bar)

			twitter_name = bing_search(current_bar) # WITH CHANGES TO TWITTER CALL FUNCTION, NEEDS REFACTORING INTO NEW FUNCTIONS
			twitter = API.user_timeline(screen_name=twitter_name, count=2)
			if twitter and verify_twitter(twitter):
				create_twitter_in_db(current_bar.google_id, twitter)
				save_twitter_attributes(current_bar.google_id, twitter)


def create_bar_in_db(current_bar):
	"""takes in current_bar object, and creates an item in the database with the desired attributes"""
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
	"""takes in current_bar object, and updates an existing item in a database with the desired fluid attributes"""
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
	""" takes in current_bar object, makes a Bing Search API call with the bar name as the search query, 
	and returns a string of the twitter url
	"""
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

				
def create_twitter_in_db(current_bar_id, twitter):
	""" takes in the id of the current bar, and the tweepy object of the twitter api call, 
	and creates the twitter item in the database
	 """
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


def save_twitter_attributes(current_bar_id, twitter):
	""" Takes in current_bar_id, and uses it to key into the Twitter table to save match attributes from the saved tweets """
	t = Twitter.objects.get(google_id=current_bar_id)
	attributes = []
	for k, v in match.ATTRIBUTE_REGISTRY.items():
		for item in v:
			if item in t.statuses.lower():
				attributes.append(k)
	if attributes:
		t.tweet_attributes = attributes
		t.save()
		
	
def verify_twitter(twitter_info):
	""" takes in a tweepy user_timeline objects, and checks match.location against the tweepy object location """
	if any(location in twitter_info[0].user.location for location in match.location):
		return True
	else:
		return False


def extract_alphanumeric_whitespace(string):
	""" takes in a string and returns the string with all non-alphanumeric characters besides spaces removed """
    return "".join([char for char in string if char in (ascii_letters + digits + ' ')])


def draw_markers(current_bars_list, request):
	""" takes in a list of Bar objects and the request to compare the 
	tweet_attributes of the current bar with the requested attributes of the post
	 """
	markers = []
	red = 'https://storage.googleapis.com/support-kms-prod/SNP_2752125_en_v0'
	green = 'https://storage.googleapis.com/support-kms-prod/SNP_2752129_en_v0'
	yellow = 'https://storage.googleapis.com/support-kms-prod/SNP_2752063_en_v0'
	input_ids = request.POST.getlist('inputs')
	for bar in current_bars_list:
		b = Bar.objects.get(google_id=bar.google_id)
		try: 
			t = Twitter.objects.get(google_id=bar.google_id)
			truth = False
			for item in input_ids:
				if item in t.tweet_attributes:
					marker = '/static/' + item + '.png'
					truth = True
					break
			if truth == False:
				marker = green
		except:
			marker = red
		markers.append([b.latitude, b.longitude, b.name, marker])
	return markers




