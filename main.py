from pprint import pprint

from bs4 import BeautifulSoup
from selenium import webdriver
import requests, time


GOOGLE_FORM_LINK = "https://forms.gle/XFKmkXfNGKdjmQrL8"
ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Accept-Language": "en-US"
}

response = requests.get(url=ZILLOW_LINK, headers=headers)
house_info = response.text
soup = BeautifulSoup(house_info, "html.parser")

all_units = soup.find_all(name="article", class_="list-card")
unit_prices = []
unit_links = []
all_unit_address = []
for unit in all_units:
    # get the price from the unit
    try:
        unit_price = unit.find(name="div", class_="list-card-price").text
        unit_prices.append(unit_price[0:6])
    except Exception as e:
        unit_prices.append("No cost listed")
    # get the link from the unit
    try:
        unit_link = unit.find(name="a", class_="list-card-link")
        unit_links.append(unit_link.get("href"))
    except Exception as e:
        unit_links.append("No link listed")
    # get the address from the unit
    try:
        unit_address = unit.find(name="address", class_="list-card-addr").text
        all_unit_address.append(unit_address)
    except Exception as e:
        all_unit_address.append("No address listed")

# gets rid of blank unit added at the end
unit_prices.pop()
unit_links.pop()
all_unit_address.pop()

time.sleep(1)

# selenium driver
chrome_driver_path = "E:\\Development\\chromedriver.exe"

driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get(GOOGLE_FORM_LINK)

for i in range(len(all_units)-1):
    address_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')
    time.sleep(1)
    address_input.send_keys(all_unit_address[i])
    price_input.send_keys(unit_prices[i])
    link_input.send_keys(unit_links[i])
    time.sleep(1)
    submit_button.click()
    time.sleep(1)
    another_response = driver.find_element_by_link_text("Submit another response")
    another_response.click()
    time.sleep(1)

driver.close()
