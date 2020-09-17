import selenium
from selenium.webdriver import Chrome
import time
import pandas as pd
import numpy as np 

def get_data(link):

	def per_page():

		time.sleep(2)

		model = []
		year = []
		color = []
		miles = []
		cost = []

		titles = driver.find_elements_by_xpath('//*[@class="listing-header"]')
		for i in titles:
			model.append(i.text)
			year.append(int(i.text.split(' ')[0]))

		colors = driver.find_elements_by_xpath('//*[@itemprop="color"]')

		for i in colors:
			color.append(i.text)

		mileage = driver.find_elements_by_xpath('//*[@class="mileage"]')

		for i in mileage:
			miles.append(i.text)

		price = driver.find_elements_by_xpath('//*[@itemprop="price"]')

		for i in price:
			cost.append(i.text)

		params = [year, color, miles, cost]

		for i in params:
			while True:
				if len(i) < len(model):
					i.append(np.nan)
				else:
					break

		entry['model'] += model
		entry['year'] += year
		entry['color'] += color
		entry['mileage'] += miles
		entry['cost'] += cost

	def turn_page():

		buttons = driver.find_elements_by_xpath('//*[@class = "pagerLink"]')
		for i in buttons:
			if i.text == '':
				i.click()
				break


	entry = {'model': [],
			 'year': [],
			 'mileage':[],
			 'color':[],
			 'cost':[]}

	driver = Chrome('./chromedriver.exe')
	driver.get(link)
		
	current_page = 1

	while True:
		print(f'page_number = {current_page}')
		per_page()
		current_page += 1
		turn_page()

		if current_page == 30:
			break

	entry = pd.DataFrame(entry)
	entry.to_csv('./Ford_resale_prices.csv', index=False)
	print(f'Collection Completed. Number of records = {len(entry)}')