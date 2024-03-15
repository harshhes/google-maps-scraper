import requests, time, csv
from bs4 import BeautifulSoup 

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

def find_element_text(driver, locator):
    try:
        element = driver.find_element(By.XPATH, locator)
        if 'button' in locator:
            return (element.get_attribute('aria-label'))[7:]
        else:
            return element.text
    except NoSuchElementException:
        return None

def scroll_down(driver):
    while True:
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 1200);")
        print("scrollll....")
        time.sleep(5)       


url = 'https://www.google.com/maps/search/breweries+in+new+york+city/@40.7262149,-74.1567273,12z/data=!4m2!2m1!6e5?entry=ttu'


# options = FirefoxOptions()
# options.add_argument("--headless")
# driver = webdriver.Firefox(options=options)
options = ChromeOptions()
driver = webdriver.Chrome(options=options, service=Service("./chromedriver"))
driver.maximize_window()
action = webdriver.ActionChains(driver)


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

driver.get(url=url)
print("getting all the breweries...")
time.sleep(4)

driver.find_element(By.XPATH, '//button[@id="searchbox-searchbutton"]').click()
time.sleep(1.5)


# el = driver.find_element(By.XPATH, '//a[@class="hfpxzc"]')
# action.move_to_element(el).perform()

# scroll_down(driver)


time.sleep(1)
driver.find_element(By.XPATH, '//a[@class="hfpxzc"]').click()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
print("scrollll....")
time.sleep(5)       



# data = []
# for link in driver.find_elements(By.XPATH, '//a[@class="hfpxzc"]'):
#     time.sleep(1)
#     link.click()
#     time.sleep(1.5)

#     try:
#         title = find_element_text(driver, '//h1[@class="DUwDvf lfPIob"]')
#         location = find_element_text(driver, '(//div[@class="Io6YTe fontBodyMedium kR99db "])[1]')
#         web = find_element_text(driver, '//div[@class="rogA2c ITvuef"]/div[1]')
#         phone = find_element_text(driver, '//button[@class="CsEnBe" and @data-tooltip="Copy phone number"]')

#         data.append({
#             "Title": title,
#             "Location": location,
#             "Phone": phone,
#             "Web": web
#         })

#         print("--------------------------")

#     except StaleElementReferenceException:
#         print("WTH gone wrong bro!!!")

#     except Exception as e:
#         print(e)
#         driver.close()

# fieldname= ['Title', "Location", "Phone", "Web"]
# with open("dataset2.csv", "w") as file:
#     writer = csv.DictWriter(file, fieldnames=fieldname)
#     writer.writeheader()
#     writer.writerows(data)


# driver.close()