import requests
from bs4 import BeautifulSoup

########################################
############# Constants ################
########################################


class PropertySearch:

    def __init__(self, url_link, headers):
        self.response = requests.get(url=url_link, headers=headers)
        self.house_info = self.response.text
        self.soup = BeautifulSoup(self.house_info, "html.parser")
        self.all_units = []
        self.unit_prices = []
        self.unit_links = []
        self.all_unit_address = []

    # find all method to locate something with a specific class
    def find_all(self, target_name, target_class):
        self.all_units = self.soup.find_all(name=target_name, class_=target_class)
        return self.all_units

    # find one item with a specific class
    def find_item(self, target_name, target_class):
        item = self.soup.find(name=target_name, class_=target_class)
        return item

    # appends the item to the list provided
    def append_item(self, custom_list, item):
        if custom_list == "unit_prices":
            self.unit_prices.append(item)
        elif custom_list == "unit_links":
            self.unit_links.append(item)
        elif custom_list == "all_unit_address":
            self.all_unit_address.append(item)
        else:
            print("Not a valid list")

    # adds all items to all the lists
    def add_unit_items(self):
        for unit in self.all_units:
            # get the price from the unit
            try:
                unit_price = unit.find(name="div", class_="list-card-price").text
                self.append_item(custom_list="unit_prices", item=unit_price[0:6])
            except Exception as e:
                self.append_item(custom_list="unit_prices", item="")
            # get the link from the unit
            try:
                unit_link = unit.find(name="a", class_="list-card-link").get("href")
                if "http" not in unit_link:
                    self.append_item(custom_list="unit_links", item=f"https://www.zillow.com{unit_link}")
                else:
                    self.append_item(custom_list="unit_links", item=unit_link)
            except Exception as e:
                self.append_item(custom_list="unit_links", item="")
            # get the address from the unit
            try:
                unit_address = unit.find(name="address", class_="list-card-addr").text
                self.append_item(custom_list="all_unit_address", item=unit_address)
            except Exception as e:
                self.append_item(custom_list="all_unit_address", item="")
            finally:
                self.unit_prices.pop()
                self.unit_links.pop()
                self.all_unit_address.pop()

    # getter for the address list
    def get_address(self, index):
        return self.all_unit_address[index]

    # getter for the link list
    def get_link(self, index):
        return self.unit_links[index]

    # getter for the price list
    def get_price(self, index):
        return self.unit_prices[index]

    # prints all lists
    def print_lists(self):
        print(f'{self.unit_prices}\n{self.unit_links}\n{self.all_unit_address}')

