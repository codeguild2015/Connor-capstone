from django.http import HttpResponse
from django.shortcuts import render
import urllib.request, json
import pprint
from login.models import Bar
import login.secrets as secrets



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
	nearby_URL2 = '&radius=500&types=bar&key='
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
	for x, y in enumerate(bars['results']):
		current_id = y['id']
		b = Bar()
		b.google_id = current_id
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
		if check_database_for_bar(current_id) == False:
			b.save()
		lst.append(b)
	return lst



def draw_markers(current_bars_list):
	markers = []
	for x in current_bars_list:
		q = Bar.objects.get(google_id=x.google_id)
		marker_coordinates = [q.latitude, q.longitude]
		markers.append(marker_coordinates)
	print(markers)
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


