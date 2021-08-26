from selenium import webdriver
from PropertySearch import PropertySearch
import time

class DriverClass:
    def __init__(self, driver, url):
        self.driver = webdriver.Chrome(executable_path=driver)
        self.driver.get(url)

    def find_x_path(self, path):
        item = self.driver.find_element_by_xpath(path)
        return item

    def find_a_path(self, path):
        item = self.driver.find_element_by_link_text(path)
        return item

    def fill_form(self, all_units_to_add, property):
        for i in range(len(all_units_to_add) - 1):
            address_input = self.find_x_path(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_input = self.find_x_path(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link_input = self.find_x_path(
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            submit_button = self.find_x_path('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')
            time.sleep(1)
            price = PropertySearch.get_price(property, i)
            address = PropertySearch.get_address(property, i)
            link = PropertySearch.get_link(property, i)
            address_input.send_keys(address)
            price_input.send_keys(price)
            link_input.send_keys(link)
            time.sleep(1)
            submit_button.click()
            time.sleep(1)
            another_response = self.find_a_path("Submit another response")
            another_response.click()
            time.sleep(1)

    def close_window(self):
        self.driver.close()

