# from selenium import webdriver

# browser = webdriver.Firefox()
# browser.get('http://localhost:8000')

# assert 'BarBird' in browser.title

# browser.quit()
from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()	

	def test_lands_on_home_page(self):
		#Thunder goes online to try the new bar app
		self.browser.get('http://localhost:8000')

		#He notices the title of the webpage is BarBird
		self.assertIn('BarBird', self.browser.title)

		#He is greeted by a main page
		#the main page has a header div
		header_text = self.browser.find_element_by_id('header_div').text
		self.assertIn('Main', header_text)

		#the main page has a main div
		maindiv = self.browser.find_element_by_id('main_div').text
		# self.assertIn('Main')

		#the main div has a textbox with placeholder 'Location'
		location_inputbox = self.browser.find_element_by_id('location')
		self.assertEqual(location_inputbox.get_attribute('placeholder'), 
			'Location'
			)

		#the main div has a button id 'search'
		search_button = self.browser.find_element_by_id('search_button')

		self.assertEqual(search_button.get_attribute('type'), 'button')
		self.assertEqual("Search", search_button.get_attribute('value'))

		#there is a div with the id 'map'
		map_div = self.browser.find_element_by_id('map')
		


		self.fail('Finish the test!')


#He enters an address for downtown portland into the search box

#The google maps element updates to show the location he searched, and populates the map with
	# x number of bars pinned in an area of y miles around him.


#when clicking on a bar, he sees the name of the bar, the twitter account, and the twitter accuracy ranking




	##search twitter based on bar name, address, state, city, etc,.
	##link twitter to bars on a green, yellow, red scale for confidence of accuracy based on
		#how many attributes were used to make the match

#The bars' pins are updated to a small image I will call BADGES depending on recent tweets.
	
	##things like 'live music', 'no cover', 'happy hour', 'ladies night' etc,.
		#Need to determine order of importance to determine which BADGE will show. ex...
			# no cover > live music > happy hour etc, or some other solution

	##recent tweets include tweets from last x hours
	##tweets are sorted through by regex for specific key words?

#Thunder sees which bar he would like to visit, and closes the webpage



'''ICING
~~~~~~~~~~~~~
#check and allow multiple browsers
#Recent searches
#Favorite bars
#Multiple Badge selection to show 'no cover' and 'live music' but filter out ladies night (hes taken)


'''

if __name__ == '__main__':
	unittest.main(warnings='ignore')
