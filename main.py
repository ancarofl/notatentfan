from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
from datetime import date
from write_to_google_sheets import main as gs_write

import os
from dotenv import load_dotenv

import constants

def get_first_int_from_string(string):
	return int((re.findall(r'\d+', string))[0])

def main():
	print("Hoi!")

	load_dotenv()
	url = os.getenv('URL')
	url2 = os.getenv('URL_2')

	date_today = date.today().strftime("%d.%m.%Y")

	results_count = 0

	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	if url:
		driver.get(url)
			
		results_element_text = (driver.find_element("xpath", '//html/body/div/main/div/div[2]/div[1]/div/div/div[1]/h1')).text
		results_count = get_first_int_from_string(results_element_text)

		print(f"On {date_today}, there are {results_count} results (URL):")
		print('')

		# TODO: This is a hack to allow the web page to load. Improve this. WebDriverWait + CSS selectors perhaps.
		time.sleep(10) # If the info for results @ beginning of list is missing, increase this to account for the page's load time

		row = 2
		for i in range(1, (results_count + 1)):
			# Ignore unexpected changes in the structure of the website.
			# Important: if any of the elements searched for (address, bedrooms etc) do not exist, that house will not be shown. 
			# I am fine with that because if those elements do not exist then it's not a match.
			# However, it could be due to a faulty data entry on the website as well (which is also why I don't filter by bedrooms + sqm).
			try:
				address = driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[1]/div[1]/div[1]/h3/a/span').text
				bedrooms = driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[1]/div[1]/div[2]/div/ul/li[2]/b').text
				is_apartment_element_text = (driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[1]/div[1]/div[1]/div/p[2]').text).lower()
				sqm_element_text = driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[1]/div[1]/div[2]/div/ul/li[3]/b').text
				sqm = get_first_int_from_string(sqm_element_text)
				price_element_text = driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[1]/div[1]/div[2]/div/ul/li[1]/b').text
				price_value = get_first_int_from_string(price_element_text)

				# TODO: Improve this...
				# Check if any elements with that XPATH exist. It would in fact be only one due to the specificity
				unavailability_label = None
				unavailability_label_elements = None
				unavailability_label_elements = driver.find_elements("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[2]/span')
				
				# If the element exists then grab the text from it
				if unavailability_label_elements and len(unavailability_label_elements) > 0:
					# print(unavailability_label_elements) # TODO: Remove debug
					unavailability_label = driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[2]/span').text
			except:
				continue

			if(is_apartment_element_text in constants.APARTMENT_LABELS and 
					int(bedrooms) == int(os.getenv('TARGET_BEDROOMS')) and
					unavailability_label is None):
				print(f"-----Apartment {i} - {price_element_text} ")
				print(address)
				print(f"{sqm} sqm")
				print(f"{bedrooms} bedrooms---")
				
				# TODO: Remove debug
				# if(unavailability_label):
					# print(unavailability_label)

				print("")

				values = [[address, sqm, bedrooms, price_value]]
				gs_write(values, row)
				row += 1

		print(f"On {date_today}, there are {row - 2} available housing options.")
	
	if url2: 
		print("")
		print("Start scrape URL_2")

		driver.get(url2)

		results_element_text = (driver.find_element("xpath", '//html/body/div[1]/div[3]/div/div[2]/div[1]/div[1]/span')).text
		results_count = get_first_int_from_string(results_element_text)

		print(f"On {date_today}, there are {results_count} results (URL2):")
		print('')

		# TODO: This is a hack to allow the web page to load. Improve this. WebDriverWait + CSS selectors perhaps.
		time.sleep(10) # If the info for results @ beginning of list is missing, increase this to account for the page's load time

		row = 2

		print("End scrape URL_2")
	
	print("Tot ziens!")

if __name__ == '__main__':
	main()
