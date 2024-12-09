import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException



class Scraper():
	def __init__(self, urls):
		# initialize class and set up a soup and page variables
		self.url = urls

		# creating a webdriver to handle a click function
		self.driver = webdriver.Firefox()
		self.driver.get(self.url)

	def __restart_func(self):
		# helping function to click a next page on site and restart function scrape_immowelt

		try:
			btn = self.driver.find_element(By.CLASS_NAME, "css-12uiy26")
			self.driver.execute_script("arguments[0].click();", btn)
			time.sleep(3)
			self.scrape_immowelt()
		except NoSuchElementException as elem:
			print("Scrapping ended.")


	def scrape_immowelt(self):

		immowelt_data = []
		keys = ["Cost", "Location", "Provider", "Rooms", "Metres", "Etage"]
		# get all data that i need to get
		try:
			url = requests.get(self.driver.current_url)

			# make a soup to get all data
			soup = BeautifulSoup(url.text, 'lxml')
			actions_list = soup.find_all("div", class_="css-79elbk")
			for action in actions_list:

				name = []
				cost = []
				location = []
				provider = []
				rooms = []
				metres = []
				etage = []
				name.append(action.find("div", class_="css-1cbj9xw").get_text())
				cost.append(action.find("div", class_="css-11nox3k").get_text())
				location.append(action.find("div", class_="css-ee7g92").get_text())
				provider.append(action.find("div", class_="css-1wek39n").get_text())
				description = action.find_all("div", class_="css-9u48bm")

				try:
					rooms.append(description[0].get_text())
					metres.append(description[2].get_text())
					etage.append(description[4].get_text())
					
					# test print
					# print(f"Cost: {cost}\nRooms : {room}\nMetres : {metres}\nEtage : {etage}\nLocation : {location}\nProvider : {provider}")
					
				except IndexError:
					# ignoring IndexError error
					pass
					# immowelt_data = {"cost": data[0], "location": data[1], "provider": data[2], "rooms": data[3], "metres": data[4], "etage": data[5]}
				for name, cost, location, provider, rooms, metres, etage in zip(name, cost, location, provider, rooms, metres, etage):

					immowelt_data.append({'Name': name, 'Cost': cost, 'Location' : location, "Provider" : provider, 'Rooms' : rooms, "Metres" : metres, "Etage" :etage})
			self.write_json(immowelt_data)
		except ElementClickInterceptedException as elem:
			print(elem)
		finally:
			# after end of scrapping first page start function to scrape next one
			self.__restart_func()
		self.driver.quit()

		self.write_json(immowelt_data)


	def write_json(self, immowelt_data, filename="immowelt.json"):

		if not os.path.exists(filename):
			with open(filename, "w") as file:

				json.dump(immowelt_data, file, indent = 4)
		else:
			with open(filename, "r+") as file:
				json.dump(immowelt_data, file, indent = 4)


if __name__ == "__main__":
	scraper = Scraper("https://www.immowelt.de/classified-search?distributionTypes=Rent&estateTypes=House,Apartment&locations=NBH2DE65431,NBH2DE65405,NBH2DE65437")
	# scraper.scrape_immowelt()
	scraper.scrape_immowelt()
	# url = scraper.scrape_immowelt()
	# scraper.scrape_immowelt(url)