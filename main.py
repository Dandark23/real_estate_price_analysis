from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt



class Scraper():
	def __init__(self, urls):
		# initialize class and set up a soup and page variables
		self.url = urls
		self.page = requests.get(self.url)
		self.soup = BeautifulSoup(self.page.text, 'lxml')


	def immowelt_scraper(self):
		# realize gathering data from a 'Immowelt' webpage

		actions_list = self.soup.find_all("div", class_="css-79elbk")
		for action in actions_list:

			cost = action.find("div", class_="css-11nox3k").get_text()
			location = action.find("div", class_="css-ee7g92").get_text()
			provider = action.find("div", class_="css-zg1vud").get_text()
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

			



if __name__ == "__main__":
	scraper = Scraper("https://www.immowelt.de/classified-search?distributionTypes=Rent&estateTypes=Apartment&locations=AD08DE1113")
	scraper.immowelt_scraper()