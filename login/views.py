from django.http import HttpResponse
from django.shortcuts import render
import urllib.request, json
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
	# coordinate_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
	# key = '&key=AIzaSyD3lM-WCdhwJtm3D3KUYNjRs3ySwWW3tm0'
	# search_text = request.POST.get('location_text', '').replace(' ', '+')

	# googleResponse = urllib.request.urlopen(coordinate_URL+search_text+key)
	# str_response = googleResponse.read().decode('utf-8') #convert googleResponse to be readable
	# jsonResponse = json.loads(str_response)
	'''
	~~~~~
	Google API commented out to limit usage. 
	~~~~~
	'''
	# latitude = str(jsonResponse['results'][0]['geometry']['location']['lat'])
	# longitude = str(jsonResponse['results'][0]['geometry']['location']['lng'])
	latitude = str(45.5164111)
	longitude = str(-122.6156611)
	formatted_latlong = latitude + ', ' + longitude
	return render(request, 'home.html', {
		'new_location_text': formatted_latlong,
		'zoom': 15
		})

def google_to_model(google_response):
	m = Bar()
	m.address = google_response['address']
	return m


