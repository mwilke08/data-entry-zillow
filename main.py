import time
from PropertySearch import PropertySearch
from DriverClass import DriverClass

# selenium driver path
CHROME_DRIVER_PATH = "E:\\Development\\chromedriver.exe"

# constants for searching property
GOOGLE_FORM_LINK = "https://forms.gle/XFKmkXfNGKdjmQrL8"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Accept-Language": "en-US"
}
ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
              "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A" \
              "-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C" \
              "%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A" \
              "%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse" \
              "%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A" \
              "%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse" \
              "%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B" \
              "%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

# create the properties class to get all data from the site
properties = PropertySearch(ZILLOW_LINK, HEADERS)
all_units = properties.find_all(target_name="article", target_class="list-card")
properties.add_unit_items()

# lets get caught up before we do all the form filling
time.sleep(1)

# creates the driver class to fill the form out
driver = DriverClass(driver=CHROME_DRIVER_PATH, url=GOOGLE_FORM_LINK)

# fills the form out through the driver class
driver.fill_form(all_units, properties)

# closes the window after the form has been filled out
driver.close_window()
