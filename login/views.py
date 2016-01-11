from django.http import HttpResponse
from django.shortcuts import render
import urllib.request, json
import pprint
from login.models import Bar
# from secrets import googlekey



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
	google_to_model(bars)

	return render(request, 'home.html', {
		'new_location_text': coordinates,
		'zoom': 15
		})

def get_google_coordinates(request):
	key = '&key=AIzaSyD3lM-WCdhwJtm3D3KUYNjRs3ySwWW3tm0'
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
	nearby_URL2 = '&radius=500&types=bar&key=AIzaSyD3lM-WCdhwJtm3D3KUYNjRs3ySwWW3tm0'

	googleResponseBars = urllib.request.urlopen(nearby_URL1+coordinates+nearby_URL2)
	str_responseBars = googleResponseBars.read().decode('utf-8')
	jsonResponseBars = json.loads(str_responseBars)
	return jsonResponseBars

	# lst = []
	# for x, y in enumerate(jsonResponseBars['results']):
	# 	lat = y['geometry']['location']['lat']
	# 	lng = y['geometry']['location']['lng']
	# 	google_id = y['id']
	# 	name = y['name']
	# 	if 'opening_hours' in y and 'open_now' in y['opening_hours']:
	# 		open_now = y['opening_hours']['open_now']
	# 	place_id = y['place_id']
	# 	if 'price_level' in y:
	# 		price_level = y['price_level']
	# 	if 'rating' in y:
	# 		rating = y['rating']
	# 	vicinity = y['vicinity']
	# 	lst.append([google_id, lat, lng, name, open_now, place_id, price_level, rating, vicinity])
	# pprint.pprint(lst)

def google_to_model(jsonResponseBars):
	for x, y in enumerate(jsonResponseBars['results']):
		b = Bar()
		b.google_id = y['id']
		b.name = y['name']
		b.latitude = y['geometry']['location']['lat']
		b.longitude = y['geometry']['location']['lng']
		if 'vicinity' in y:
			b.vicinity = y['vicinity']
		if 'price_level' in y:
			b.price_level = y['price_level']
		if 'rating' in y:
			b.rating = y['rating']
		if 'opening_hours' in y and 'open_now' in y['opening_hours']:
			b.open_at_update = y['opening_hours']['open_now']
		b.save()




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


