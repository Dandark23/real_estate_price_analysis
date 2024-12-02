import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
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

		self.driver = webdriver.Firefox()
		self.driver.get(self.url)
		# self.page = requests.get(self.url)
		# self.soup = BeautifulSoup(self.page.text, 'lxml')


	def scrape_immowelt(self):
		# realize gathering data from a 'Immowelt' webpage

		pass

	def __restart_func(self):

		btn = self.driver.find_element(By.CLASS_NAME, "css-12uiy26")
		self.driver.execute_script("arguments[0].click();", btn)
		time.sleep(3)

		self.webdriver_immowelt()

	def webdriver_immowelt(self):
		# creating a webdriver to handle a click function

		curr_url = []

		btn = self.driver.find_element(By.CLASS_NAME, "css-12uiy26")
		while btn != None:
			try:
				url = requests.get(self.driver.current_url)

				soup = BeautifulSoup(url.text, 'lxml')
				actions_list = soup.find_all("div", class_="css-79elbk")
				for action in actions_list:

					cost = action.find("div", class_="css-11nox3k").get_text()
					location = action.find("div", class_="css-ee7g92").get_text()
					provider = action.find("div", class_="css-1wek39n").get_text()
					description = action.find_all("div", class_="css-9u48bm")

					try:
						room = description[0].get_text()
						metres = description[2].get_text()
						etage = description[4].get_text()
						print(f"Cost: {cost}\nRooms : {room}\nMetres : {metres}\nEtage : {etage}\nLocation : {location}\nProvider : {provider}")
					except IndexError:
						pass
					
				if btn == None:
					print("-----------Immowelt data crawl ended.-----------")
				else:
					print("/////////////////////////////////////////////////////////////////////////////////////////////")
					self.__restart_func()

			except NoSuchElementException as elem:  
				# print("No such element : ", elem)
				break
			except ElementClickInterceptedException as elem:
				print(elem)
				break
			finally:
				curr_url.append(self.driver.current_url)
				print(curr_url)
		self.driver.quit()

		return curr_url



if __name__ == "__main__":
	scraper = Scraper("https://www.immowelt.de/classified-search?distributionTypes=Rent&estateTypes=House,Apartment&locations=AD08DE1113&order=Default&m=homepage_new_search_classified_search_result")
	# scraper.scrape_immowelt()
	scraper.webdriver_immowelt()
	# url = scraper.webdriver_immowelt()
	# scraper.scrape_immowelt(url)