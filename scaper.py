from selenium import webdriver
import time
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as chromeOptions

book_data = {
    "titles" : [],
    "prices" : [],
    "availability" : []
}

options = chromeOptions()
#options.add_argument("--headless")
options.add_argument("log-level=3") #Deprecated error messages are driving me insane


driver = webdriver.Chrome(options=options)

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
    print(len(elements))
    for element in elements:
        print(element.text)



def next_page():
    nextButton = driver.find_element(By.LINK_TEXT, 'next')
    nextButton.click()

def go_to_philosophy_page():
    philosphyButton = driver.find_element(By.LINK_TEXT, 'Philosophy')
    philosphyButton.click()
    




def main():
    driver.get('https://books.toscrape.com')
    time.sleep(5)
    go_to_philosophy_page()
    driver.quit()

if __name__ == "__main__":
    main()