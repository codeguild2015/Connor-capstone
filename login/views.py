from django.http import HttpResponse
from django.shortcuts import render
import urllib.request, json
import pprint
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


	nearby_URL1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
	nearby_URL2 = '&radius=500&types=bar&key=AIzaSyD3lM-WCdhwJtm3D3KUYNjRs3ySwWW3tm0'

	googleResponseBars = urllib.request.urlopen(nearby_URL1+coordinates+nearby_URL2)
	str_responseBars = googleResponseBars.read().decode('utf-8')
	jsonResponseBars = json.loads(str_responseBars)

	# pprint.pprint(jsonResponseBars['results'][0])
	lst = []
	for x, y in enumerate(jsonResponseBars['results']):
		lat = y['geometry']['location']['lat']
		lng = y['geometry']['location']['lng']
		gId = y['id']
		name = y['name']
		# open_now = y['opening_hours']['open_now']
		place_id = y['place_id']
		# price_level = y['price_level']
		# rating = y['rating']
		vicinity = y['vicinity']
		lst.append([gId, lat, lng, name, place_id, vicinity])
	pprint.pprint(lst)



	'''
	~~~~~
	Google API commented out to limit usage. 
	~~~~~
	'''

	return render(request, 'home.html', {
		'new_location_text': coordinates,
		'zoom': 15
		})

def google_to_model(google_response):
	m = Bar()
	m.address = google_response['address']
	return m



#to pull from DB MAYBE?!
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


