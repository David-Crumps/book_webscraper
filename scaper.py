from selenium import webdriver
import time
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.common.exceptions import NoSuchElementException

'''
def find_all_ids():
     elements = driver.find_elements(By.XPATH, '//*[@id]')
     for element in elements:
         print(element.get_attribute('id'))

#Book titles stored between 'h3' tags, which contain 'a' tags, which hold the title
def get_book_titles_on_page():
    h3_elements = driver.find_elements(By.TAG_NAME, 'h3')
    if h3_elements:
        for element in h3_elements:
            a_tag = element.find_element(By.TAG_NAME, 'a')
            print(a_tag.get_attribute('title'))
    else:
        print("No h3 elements found on this page")

def get_prices_on_page():
    elements = driver.find_elements(By.CLASS_NAME, "price_color")
    for element in elements:
        print(element.text)

def get_availability_on_page():
    elements = driver.find_elements(By.CSS_SELECTOR, "p.instock.availability")
    for element in elements:
        print(element.text)

def go_to_philosophy_page():
    philosphyButton = driver.find_element(By.LINK_TEXT, 'Philosophy')
    philosphyButton.click()
'''
    
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
    scraper = BookScraper("https://books.toscrape.com", False)
    scraper.scrapeAllPages()
    scraper.close()

    for key, value in scraper.bookData.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()