print("Hoi!")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
from datetime import date

import os
from dotenv import load_dotenv
load_dotenv()

# Deprecated since https://github.com/SeleniumHQ/selenium/blob/d6acda7c0254f9681574bf4078ff2001705bf940/py/CHANGES#L101
#PATH = r"D:\chromedriver"
#driver = webdriver.Chrome(PATH)
  
url = os.getenv('URL')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)
  	  
results_element_text = (driver.find_element("xpath", '//html/body/div/main/div/div[2]/div[1]/div/div/div[1]/h1')).text
results_count = int((re.findall(r'\d+', results_element_text))[0])

date_today = date.today().strftime("%d.%m.%Y")

print(f"On {date_today}, there are {results_count} results:")
print('')

 # TODO: This is a hack to allow the web page to load. Improve this. WebDriverWait + CSS selectors perhaps.
time.sleep(10) # If the info for results @ beginning of list is missing, increase this to account for the page's load time

for i in range(1, (results_count + 1)):		  	  
	# Ignore unexpected changes in the structure of the website.
	# Important: if any of the elements searched for (address, bedrooms etc) do not exist, that house will not be shown. 
	# I am fine with that because if those elements do not exist then it's not a match.
	# However, it could be due to a faulty data entry on the website as well (which is also why I don't filter by bedrooms + sqm).
	try:
		address = driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[1]/div[1]/div[1]/h3/a/span').text
		bedrooms = driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[1]/div[1]/div[2]/div/ul/li[2]/b').text
		is_apartment = (driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[1]/div[1]/div[1]/div/p[2]').text).lower() == 'apartment'
		sqm_element_text = driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[1]/div[1]/div[2]/div/ul/li[3]/b').text
		sqm = int((re.findall(r'\d+', sqm_element_text))[0])
		price = driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[1]/div[1]/div[2]/div/ul/li[1]/b').text
		# availability = driver.find_element("xpath", f'//html/body/div/main/div/div[2]/div[2]/div[2]/div/ul/li[{i}]/article/div[2]/span').text
	except:
		continue

	# TODO: Filter by availability.
	if(is_apartment):	
		print(f"-----Apartment {i} - {price} ")
		print(address)
		print(f"{sqm} sqm")
		print(f"{bedrooms} bedrooms---")

		print("")

print("Tot ziens!")
