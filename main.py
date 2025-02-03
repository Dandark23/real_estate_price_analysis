import requests
import pandas as pd
import time
from datetime import datetime 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options


# options for a webdriver 
firefox_options = Options()
# setting a webdriver to a headless mode to make all work faster
firefox_options.add_argument("--headless")
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0"
firefox_options.add_argument(f"--user-agent={user_agent}")


class ImmoweltSpider():
	def __init__(self, url):
		"""initialize class and set up a soup and page variables"""
		self.url = url

		# creating a webdriver to handle a click function
		self.driver = webdriver.Firefox(options=firefox_options)
		self.driver.get(self.url)
		self.raw_immowelt_data = []

		self.raw_csv_data = []


	def __restart_func(self):
		"""helping function to click a next page on site and restart function scrape_immowelt"""

		try:
			btn = self.driver.find_element(By.CLASS_NAME, "css-12uiy26")
			self.driver.execute_script("arguments[0].click();", btn)
			time.sleep(3)
			self.scrape()
		except NoSuchElementException as elem:
			pass


	def scrape(self):
		"""Function that make extraction of all the data"""
		try:
			url = requests.get(self.driver.current_url)

			# make a soup to get all data
			soup = BeautifulSoup(url.text, 'lxml')
			actions_list = soup.find_all("div", class_="css-79elbk")
			for action in actions_list:

				# lists for data
				cost = []
				location = []
				providers = []
				rooms = []
				raw_metres = []
				metres = []
				action_url = []

				cost.append(action.find("div", class_="css-11nox3k").get("aria-label"))
				location.append(action.find("div", class_="css-4udngo").get_text())
				providers.append(action.find("div", class_="css-1wek39n").get_text())

				raw_action_url = action.find("a", class_="css-xt08q3")
				action_url.append(raw_action_url['href'])
				description = action.find_all("div", class_="css-9u48bm")

				try:
					# checking what data is in description list. if Zimmer in 0 then its room else it's metres 
					if "Zimmer" in description[0].get_text():
						rooms.append(description[0].get_text())
						raw_metres.append(description[2].get_text())
					else:
						raw_metres.append(description[0].get_text())
						rooms.append("None")
						
					# changing comma to a unicode nine version comma for good .csv
					for m in raw_metres:
						m = m.replace(",","\u201A")

						metres.append(m)
				except IndexError:
					print("Lack of some data")
				# append a data one by one to a raw data list
				for cost, location, providers, rooms, metres, action_url in zip(cost, location, providers, rooms, metres, action_url):
					self.raw_immowelt_data.append({'Cost': cost, 'Location' : location, 'Provider' : providers, 'Rooms' : rooms, 'Metres' : metres, 'Url' : action_url})
		except ElementClickInterceptedException as elem:
			print(elem)
		except AttributeError:
			pass
		finally:
			# after end of scrapping first page start restart function to scrape next one
			self.__restart_func()
		self.driver.quit()
		for value in self.raw_immowelt_data:
			self.raw_csv_data.append(value.values())

		return self.raw_csv_data

class DataFrameProcessor():

	def __init__(self, raw_data):
		self.raw_data = raw_data

	def make_dataframe(self, filename):
		"""Convert extracted data into .csv file"""
		df = pd.DataFrame(self.raw_data)
		df.columns = ["Cost", "Location", "Provider", "Rooms", "Metres", "Url"]
		df.to_csv(filename, index=False)


def log_progress(message):
	''' This function logs the mentioned message of a given stage of the code execution to a log file. Function returns nothing'''
	timestamp_format  = "%Y-%b-%d-%H:%M:%S"#year-month-day-hour:minute:seconds
	now = datetime.now()
	timestamp = now.strftime(timestamp_format)
	print(message)
	with open("code_log.txt", "a") as file:
		file.write(f"{timestamp} : {message}\n")

if __name__ == "__main__":

	# make immowelt spider
	log_progress("Starting data extraction.")
	# enter a url with needed options for search 
	immowelt_spider = ImmoweltSpider("https://www.immowelt.de/classified-search?distributionTypes=Rent&estateTypes=House,Apartment&locations=NBH2DE75688,NBH2DE75641,NBH2DE75631,NBH2DE75638&numberOfRoomsMax=2&priceMax=1500")
	# start extracting data 
	raw_data = immowelt_spider.scrape()
	log_progress("Data extraction complete.")


	# create a instance of DataFrameProcessor class
	dataframe_processor = DataFrameProcessor(raw_data)
	# enter a location for extracted data in .csv file format
	dataframe_processor.make_dataframe("C:/your/root/to/file/fileName.csv")
	log_progress("Creating DataFrame Object.")