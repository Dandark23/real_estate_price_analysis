import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



class Scraper():
	def __init__(self):
		# initialize class and set up a soup and page variables
		pass


	def scrape_immowelt(self, urls):
		# realize gathering data from a 'Immowelt' webpage
		self.url = urls
		self.page = requests.get(self.url)
		self.soup = BeautifulSoup(self.page.text, 'lxml')

		actions_list = self.soup.find_all("div", class_="css-79elbk")
		for action in actions_list:

			cost = action.find("div", class_="css-11nox3k").get_text()
			location = action.find("div", class_="css-ee7g92").get_text()
			provider = action.find("div", class_="css-1wek39n").get_text()
			description = action.find_all("div", class_="css-9u48bm")
			try:
				room = description[0].get_text()
				metres = description[2].get_text()
				etage = description[4].get_text()
			except IndexError:
				room = None
				metres = None
				etage = None
				location = None
			print(f"Cost: {cost}\nRooms : {room}\nMetres : {metres}\nEtage : {etage}\nLocation : {location}\nProvider : {provider}")
		
		btn = self.soup.find("button", class_="css-12uiy26")
		if btn == None:
			print("-----------Immowelt data crawl ended.-----------")
		else:
			btn = None
			self.webdriver_immowelt()
			print("/////////////////////////////////////////////////////////////////////////////////////////////")


	def webdriver_immowelt(self):
		# creating a webdriver to handle a click function
		driver = webdriver.Firefox()
		driver.get(self.url)

		driver.find_element(By.CLASS_NAME, "css-12uiy26").click()
		time.sleep(5)
		curr_url = driver.current_url
		driver.close()

		return curr_url

			



if __name__ == "__main__":
	scraper = Scraper()
	scraper.scrape_immowelt("https://www.immowelt.de/classified-search?distributionTypes=Rent&estateTypes=Apartment&locations=NBH2DE65431,NBH2DE65405,NBH2DE65407")
	url = scraper.webdriver_immowelt()
	scraper.scrape_immowelt(url)