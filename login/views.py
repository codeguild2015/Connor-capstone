from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from login.models import Bar

import urllib.request, json
import pprint
import login.secrets as secrets
import login.matching_libraries as match
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
	marker_coordinates = draw_markers(current_bars_list)
	assign_twitter_in_db(current_bars_list)

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
	# latitude = str(45.5164111)
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

def check_database_for_bar(current_id):
		if Bar.objects.filter(google_id=current_id):
			return True
		else:
			return False

def google_to_model(bars):
	lst = []
	for x, json in enumerate(bars['results']):
		current_id = json['id']
		b = Bar()
		b.google_id = current_id
		b.name = json['name']
		b.stripped_name = extract_alphanumeric(json['name'].lower())
		b.latitude = json['geometry']['location']['lat']
		b.longitude = json['geometry']['location']['lng']
		if 'vicinity' in json:
			b.vicinity = json['vicinity']
		if 'price_level' in json:
			b.price_level = json['price_level']
		if 'rating' in json:
			b.rating = json['rating']
		if 'opening_hours' in json and 'open_now' in json['opening_hours']:
			b.open_at_update = json['opening_hours']['open_now']
		b.creation_date = timezone.now()
		b.updated_date = timezone.now()

		if check_database_for_bar(current_id) == False: #means Bar isn't in DB
			b.save()  
		else:
			update_bar_in_db(json, current_id)
		lst.append(b)
	return lst

def update_bar_in_db(json, current_id):
	b = Bar.objects.get(google_id=current_id)
	b.updated_date = timezone.now()
	if 'price_level' in json:
		b.price_level = json['price_level']
	if 'rating' in json:
		b.rating = json['rating']
	if 'opening_hours' in json and 'open_now' in json['opening_hours']:
		b.open_at_update = json['opening_hours']['open_now']
	b.save()

def assign_twitter_in_db(current_bars_list):
	consumer_key = secrets.consumer_key
	consumer_secret = secrets.consumer_secret
	access_token = secrets.access_token
	access_secret = secrets.access_secret

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	api = tweepy.API(auth)

	# stripped = []
	# stripped_plus_bar = []
	# stripped_plus_pdx = []
	# for bar in current_bars_list:
	stripped = Matching(current_bars_list)
	stripped_plus_bar = Matching(current_bars_list, 'bar')
		# stripped_plus_bar.append(extract_alphanumeric(bar.name + 'bar').lower())
		# stripped_plus_pdx.append(extract_alphanumeric(bar.name + 'pdx').lower())
	# for x in stripped.name.values():
	# 	print(x.name, x.id)
	# print(stripped.name, stripped.id)
	# for x in stripped:
	# 	print(x.name, x.id)
	# print(stripped.name)
	# matches = []

	def verify_stripped(stripped):
		twitters = api.lookup_users(screen_names=stripped.name)
		for a, user in enumerate(twitters):
			for location in match.location:
				if location in user.location:
					# pass
					pp = stripped.name.index(user.screen_name.lower())
					print(pp, stripped.name[pp], stripped.id[pp])
					# matches.append([user.location, user.id_str, user.screen_name.lower()])

	# def verify_stripped_plus_bar(stripped_plus_bar):
	# 	# print(stripped_plus_bar.name)
	# 	twitters = api.lookup_users(screen_names=stripped_plus_bar.name)
	# 	for a, user in enumerate(twitters):
	# 		for location in match.location:
	# 			if location in user.location:
	# 				# pass
	# 				print(stripped_plus_bar.name[a], stripped_plus_bar.id[a])
					# matches.append([user.location, user.id_str, user.screen_name.lower()])

	# def verify_stripped_plus_bar():
	# 	twitters = api.lookup_users(screen_names=stripped_plus_bar)
	# 	for user in twitters:
	# 		for location in match.location:
	# 			if location in user.location:
	# 				matches.append([user.location, user.id_str, user.screen_name.lower()])

	# def verify_stripped_plus_pdx():
	# 	twitters = api.lookup_users(screen_names=stripped_plus_pdx)
	# 	for user in twitters:
	# 		for location in match.location:
	# 			if location in user.location:
	# 				matches.append([user.location, user.id_str, user.screen_name.lower()])


	verify_stripped(stripped)
	# verify_stripped_plus_bar(stripped_plus_bar)
	# verify_stripped_plus_pdx()
	# print(matches)


def extract_alphanumeric(string):
    return "".join([char for char in string if char in (ascii_letters + digits)])

def draw_markers(current_bars_list):
	markers = []
	for x in current_bars_list:
		q = Bar.objects.get(google_id=x.google_id)
		marker_coordinates = [q.latitude, q.longitude]
		markers.append(marker_coordinates)
	return markers


class Matching():
	def __init__(self, bar, addition=""):
		self.name = [extract_alphanumeric(x.name + addition).lower() for x in bar]
		self.id = [y.google_id for y in bar]


