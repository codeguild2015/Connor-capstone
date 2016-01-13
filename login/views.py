from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from login.models import Bar

import login.secrets as secrets
import login.matching_libraries as match

import urllib.request, json
import requests
from requests.auth import HTTPBasicAuth

import pprint
import datetime
import tweepy
from string import ascii_letters, digits


# Create your views here.
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
	current_bars_list = google_to_model(bars)
	

	possible_twitters = check_database_for_bar(current_bars_list)
	existing_accounts = verify_possible_twitters(possible_twitters)
	get_twitter_match_object(possible_twitters, existing_accounts)
	marker_coordinates = draw_markers(current_bars_list)

	# possible_twitters = get_list_of_possible_twitters(current_bars_list)
	# existing_accounts = verify_possible_twitters(possible_twitters)
	# get_twitter_match_object(possible_twitters, existing_accounts)

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


def google_to_model(bars):
	current_bars = [CurrentBar(bar) for bar in bars['results']] 
	# current_bars = [CurrentBar(bars['results'][1])] #USED TO LIMIT BARS RETURNED TO 1
	# check_database_for_bar(current_bars)
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
	bing_results = []
	for current_bar in current_bars:
		# print(current_bar.name)
		if Bar.objects.filter(google_id=current_bar.google_id):
			update_bar_in_db(current_bar)
		else:
			create_bar_in_db(current_bar)
			bing_results.append(TwitterAccount(bing_search(current_bar), current_bar.google_id))
	# for item in bing_results:
	# 	print(item.name, item.google_id)
	return bing_results

def create_bar_in_db(current_bar):
	# print('hello')
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
		return bing_result['d']['results'][0]['Url'].rsplit('/', 1)[-1]

def extract_alphanumeric_whitespace(string):
    return "".join([char for char in string if char in (ascii_letters + digits + ' ')])

def draw_markers(current_bars_list):
	markers = []
	for x in current_bars_list:
		q = Bar.objects.get(google_id=x.google_id)
		marker_coordinates = [q.latitude, q.longitude]
		markers.append(marker_coordinates)
	return markers

# def get_list_of_possible_twitters(current_bars_list):
# 	possible_twitters = []
# 	for bar in current_bars_list:
# 		possible_twitters.append(TwitterMatch(bar))
# 		possible_twitters.append(TwitterMatch(bar, 'bar'))
# 		possible_twitters.append(TwitterMatch(bar, 'pdx'))
# 	return possible_twitters

# class TwitterMatching():
# 	def __init__(self, bar, addition=""):
# 		self.name = bar.stripped_name + addition
# 		self.id = bar.google_id

class TwitterAccount():
	def __init__(self, twitter, google_id):
		self.name = twitter
		self.google_id = google_id

def verify_possible_twitters(possible_twitters): # NOT GETTING ANYTHING PASSED IN
	consumer_key = secrets.consumer_key
	consumer_secret = secrets.consumer_secret
	access_token = secrets.access_token
	access_secret = secrets.access_secret

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	api = tweepy.API(auth)

	verified_accounts = []
	# for twitter in possible_twitters:
	# 	print(twitter.name, twitter.google)
	# print(possible_twitters)
	# for item in possible_twitters:
	# 	print(item.name)
	names = [twitter.name for twitter in possible_twitters]
	# print(names)
	twitters = api.lookup_users(screen_names=names)
	for user in twitters:
		# for location in match.location:
		# if location in user.location.lower():
		if any(location in user.location.lower() for location in match.location):
			verified_accounts.append(user.screen_name)
	# print(verified_accounts)
	return verified_accounts

# def verify_possible_twitters(possible_twitters):
# 	consumer_key = secrets.consumer_key
# 	consumer_secret = secrets.consumer_secret
# 	access_token = secrets.access_token
# 	access_secret = secrets.access_secret

# 	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# 	auth.set_access_token(access_token, access_secret)

# 	api = tweepy.API(auth)

# 	verified_accounts = []
# 	names = [bar.name for bar in possible_twitters]
# 	twitters = api.lookup_users(screen_names=names)
# 	for user in twitters:
# 		for location in match.location:
# 			if location in user.location:
# 				verified_accounts.append(user.screen_name.lower())	
# 	return verified_accounts

def get_twitter_match_object(possible_twitters, verified_accounts):
	matches = []
	print(verified_accounts)
	for item in possible_twitters:
		print(item.name)
		if item.name in verified_accounts:
			matches.append([item.name, item.google_id])
	print(matches)



