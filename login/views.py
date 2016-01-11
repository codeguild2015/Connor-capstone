from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
import urllib.request, json
import pprint
from login.models import Bar
import login.secrets as secrets
import datetime



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
	updates = Bar.objects.get(google_id=current_id)
	updates.updated_date = timezone.now()
	if 'price_level' in json:
		updates.price_level = json['price_level']
	if 'rating' in json:
		updates.rating = json['rating']
	if 'opening_hours' in json and 'open_now' in json['opening_hours']:
		updates.open_at_update = json['opening_hours']['open_now']
	updates.save()



def draw_markers(current_bars_list):
	markers = []
	for x in current_bars_list:
		q = Bar.objects.get(google_id=x.google_id)
		marker_coordinates = [q.latitude, q.longitude]
		markers.append(marker_coordinates)
	return markers




# to pull from DB MAYBE?!
# class Bar():
# 	def __init__(self):
# 		self.gId = Bar.objects.get().gId
# 		self.name = Bar.objects.get().name
# 		self.latitude = Bar.objects.get().latitude
# 		self.longitude = Bar.objects.get().longitude
# 		self.vicinity = Bar.objects.get().vicinity
# 		self.price_level = Bar.objects.get().price_level
# 		self.rating = Bar.objects.get().rating
# 		self.creation_date = Bar.objects.get().creation_date
# 		self.updated_date = Bar.objects.get().updated_date
# 		self.open_at_update = Bar.objects.get().open_at_update


