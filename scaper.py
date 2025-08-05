from selenium import webdriver
import time
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

#Should take in a dataframe object
def exportToExcel(dataFrame):
    dataFrame.to_excel("scraped_books.xlsx", index=False, engine='openpyxl')
       
class BookScraper:
    def __init__(self, baseUrl, headless=True):
        self.baseUrl = baseUrl

        self.bookData = {
            "title" : [],
            "price" : [],
            "availability" : []
        }

        options = chromeOptions()
        options.add_argument("log-level=3")
        if headless:
            options.add_argument("--headless")
                
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.baseUrl)
        time.sleep(5)
    
    def scrapeCurrentPage(self):
        books = self.driver.find_elements(By.CLASS_NAME, "product_pod")
        for book in books:
            try:
                title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
                price = book.find_element(By.CLASS_NAME, "price_color").text
                availability = book.find_element(By.CSS_SELECTOR, "p.instock.availability").text.strip()

                self.bookData["title"].append(title)
                self.bookData["price"].append(price)
                self.bookData["availability"].append(availability)
            except Exception as e:
                print(f"Error scraping book: {e}")
    
    def scrapeAllPages(self):
        canNext = True
        while canNext:
            self.scrapeCurrentPage()
            canNext = self.nextPage()
    
    def getData(self):
        return pd.DataFrame(self.bookData)

    def nextPage(self):
        try:
            next_button = self.driver.find_element(By.LINK_TEXT, "next")
            next_button.click()
            time.sleep(5)
        except NoSuchElementException:
            return False
        return True

    def close(self):
        self.driver.quit()






def main():
    #scraper = BookScraper("https://books.toscrape.com", False)
    #scraper.scrapeAllPages()
    #scraper.close()
    #exportToExcel(scraper.getData())
    print("Hi")

if __name__ == "__main__":
    main()