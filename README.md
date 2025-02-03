Real Estate Price Analysis

Description: 
    Real Estate Price Analysis is project for searching appartaments\houses data on Immowelt website, for a further data working purpouses.

Installation:
    On your terminal:
    1. git clone https://github.com/Dandark23/real_estate_price_analysis
    2. cd your-project-name
    3. pip install -r requirements.txt

Execution:
    1. into variable "immowelt_spider" into class "ImmoweltSpider" push url of Immowelt website with selected by you filters of search.
    (example - City: Berlin; Neighborhood: Adlershof, Karow, Blankenfelde, Gesundbrunnen; Rooms: 2; Cost: Max: 1500$)
    
    2. execute project in bash\cmd terminal\powershell through "python main.py"
    
    3. in dataframe_processor.make_dataframe("C:/your/root/to/file/fileName") enter root where to create a .csv file
    
    4. after program executed get .csv file 

Used technologies:
    Pandas library for creating a dataframe object and good .csv creation
    Selenium library for creating a webdriver object to work with more pages at one time
    BeautifulSoup library for scraping data from webpage

