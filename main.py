import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
import json
import os
import scrapy
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
		self.raw_immowelt_data = []


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

		try:
			url = requests.get(self.driver.current_url)

			# make a soup to get all data
			soup = BeautifulSoup(url.text, 'lxml')
			actions_list = soup.find_all("div", class_="css-79elbk")
			for action in actions_list:

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
					provider = provider.replace("\u00ad", " ")
					providers.append(provider)

				raw_action_url = action.find("a", class_="css-xt08q3")
				action_url.append(raw_action_url['href'])
				description = action.find_all("div", class_="css-9u48bm")

				try:
					rooms.append(description[0].get_text())
					raw_metres.append(description[2].get_text())
					for m in raw_metres:
						m = m.replace('\u00b2', '2')
						metres.append(m)
					
					# test print
					# print(f"Cost: {cost}\nRooms : {room}\nMetres : {metres}\nEtage : {etage}\nLocation : {location}\nProvider : {provider}")
					for cost, location, providers, rooms, metres, action_url in zip(cost, location, providers, rooms, metres, action_url):
						self.raw_immowelt_data.append({'Cost': cost, 'Location' : location, "Provider" : providers, 'Rooms' : rooms, "Metres" : metres, "Url " : action_url})
					
				except IndexError:
					# ignoring IndexError error
					pass
					# immowelt_data = {"cost": data[0], "location": data[1], "provider": data[2], "rooms": data[3], "metres": data[4], "etage": data[5]}
		except ElementClickInterceptedException as elem:
			print(elem)
		finally:
			# after end of scrapping first page start function to scrape next one
			# return raw_immowelt_data
			self.__restart_func()
		self.driver.quit()
		self.write_json(self.raw_immowelt_data)


	def write_json(self, immowelt_data, filename="immowelt.json"):

		if not os.path.exists(filename):
			with open(filename, "w", encoding="utf-8") as file:

				json.dump(immowelt_data, file, ensure_ascii=False, indent = 4)
		else:
			with open(filename, "r+", encoding="utf-8") as file:
				json.dump(immowelt_data, file, ensure_ascii=False, indent = 4)


if __name__ == "__main__":
	scraper = Scraper("https://www.immowelt.de/classified-search?distributionTypes=Rent&estateTypes=House,Apartment&locations=NBH2DE65431,NBH2DE65405,NBH2DE65407,NBH2DE65437")
	# scraper.scrape_immowelt()
	scraper.scrape_immowelt()
	# url = scraper.scrape_immowelt()
	# scraper.scrape_immowelt(url)