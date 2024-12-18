import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
import json
import csv
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


def write_json(immowelt_data, filename=""):
	# write function 
	if not os.path.exists(filename):
		with open(filename, "w", encoding="utf-8") as file:

			json.dump(immowelt_data, file, ensure_ascii=False, indent = 4)
	else:
		with open(filename, "r+", encoding="utf-8") as file:
			json.dump(immowelt_data, file, ensure_ascii=False, indent = 4)

# WIP!!!!!!!!!!!!!
def write_csv(headers, data, filename=""):
	if not os.path.exists(filename):
		with open(filename, "w", encoding="utf-8", newline='') as file:
			writer = csv.writer(file, delimiter=",")
			writer.writerow(headers)
			writer.writerows(data)
	else:
		with open(filename, "r+", newline='') as file:
			writer = csv.writer(file, delimiter=",")
			writer.writerow(headers)
			writer.writerows(data)
			

class ImmoweltSpider():
	def __init__(self, url):
		# initialize class and set up a soup and page variables
		self.url = url

		# creating a webdriver to handle a click function
		self.driver = webdriver.Firefox()
		self.driver.get(self.url)
		self.raw_immowelt_data = []

		self.raw_csv_data = []


	def __restart_func(self):
		# helping function to click a next page on site and restart function scrape_immowelt

		try:
			btn = self.driver.find_element(By.CLASS_NAME, "css-12uiy26")
			self.driver.execute_script("arguments[0].click();", btn)
			time.sleep(3)
			self.scrape()
		except NoSuchElementException as elem:
			print("Scrapping ended.")


	def scrape(self):

		try:
			url = requests.get(self.driver.current_url)

			# make a soup to get all data
			soup = BeautifulSoup(url.text, 'lxml')
			actions_list = soup.find_all("div", class_="css-79elbk")
			for action in actions_list:

				# lists for data
				cost = []
				location = []
				raw_providers = []
				providers = []
				rooms = []
				metres = []
				raw_metres = []
				action_url = []

				cost.append(action.find("div", class_="css-11nox3k").get("aria-label"))
				location.append(action.find("div", class_="css-4udngo").get_text())
				raw_providers.append(action.find("div", class_="css-1wek39n").get_text())
				for provider in raw_providers:
					# replacing weird unicode with a white space
					provider = provider.replace("\u00ad", " ")
					providers.append(provider)

				raw_action_url = action.find("a", class_="css-xt08q3")
				action_url.append(raw_action_url['href'])
				description = action.find_all("div", class_="css-9u48bm")

				try:
					rooms.append(description[0].get_text())
					raw_metres.append(description[2].get_text())
					# replacing a unicode square symbol to a just number 2 so json won't see any unicode
					for m in raw_metres:
						m = m.replace('\u00b2', '2')
						metres.append(m)
					# append a data one by one to a raw data list
					for cost, location, providers, rooms, metres, action_url in zip(cost, location, providers, rooms, metres, action_url):
						self.raw_immowelt_data.append({'Cost': cost, 'Location' : location, "Provider" : providers, 'Rooms' : rooms, "Metres" : metres, "Url " : action_url})

					
				except IndexError:
					# ignoring IndexError error
					pass
		except ElementClickInterceptedException as elem:
			print(elem)
		finally:
			# after end of scrapping first page start function to scrape next one
			# return raw_immowelt_data
			self.__restart_func()
		self.driver.quit()
		write_json(self.raw_immowelt_data, filename="immowelt.json")
		
		# WIP!!!!!!!!!!!!!
		header = ['Cost', 'Location', 'Provider', 'Rooms', 'Metres', 'Url']
		for value in self.raw_immowelt_data:
			self.raw_csv_data.append(value.values())
		write_csv(header, self.raw_csv_data, filename="immowelt_data.csv")

# WIP!!!!!!!!!!!!!
class AutoScoutSpider():

	def __init__(self, url):
		self.url = url

		self.driver = webdriver.Firefox()
		self.driver.get(self.url)

	
	def scrape(self):
		url = requests.get(self.driver.current_url)
		print(url.status_code)
		soup = BeautifulSoup(url.text, "lxml")
		data = soup.find_all("li", class_="result-list__listing ")
		for i in data:
			print(i)

if __name__ == "__main__":
	immowelt_spider = ImmoweltSpider("https://www.immowelt.de/classified-search?distributionTypes=Rent&estateTypes=House,Apartment&locations=NBH2DE65431,NBH2DE65405,NBH2DE65407,NBH2DE65437")
	immowelt_spider.scrape()

	# autoscout_spider = AutoScoutSpider("https://www.immobilienscout24.de/Suche/de/hamburg/hamburg/altona/ottensen/wohnung-mieten?pricetype=rentpermonth&enteredFrom=result_list")
	# autoscout_spider.scrape()