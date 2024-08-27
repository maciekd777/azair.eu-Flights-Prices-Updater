import csv
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from constants import ID_SPLITTER, SAVED_DATA_PATH, FIELDNAMES
from currency_converter import CurrencyConverter


class NewDataParser:
    def __init__(self):
        self.url = None
        self.cities_from = []
        self.cities_to = []
        self.id_list = []
        self.dates = []
        self.len_of_stay_list = []
        self.there_price_list = []
        self.back_price_list = []
        self.total_price_list = []
        self.data_to_print = {
            "From": self.cities_from,
            "To": self.cities_to,
            "Date": self.dates,
            "Length of stay": self.len_of_stay_list,
            "Total price": self.total_price_list
        }
        self.data_to_save = []

    @staticmethod
    def get_url():
        while True:
            u = input("\nInput azair.eu search results meeting following requirements:\n"
                            "* English version of the site\n"
                            "* Include return flight\n"
                            "* Only direct flights: ")

            requirements = [
                    r"^(?:https://|http://)?(www\.)?azair\.eu",
                    r"&lang=en&",
                    r"&isOneway=return&",
                    r"&maxChng=0&"
            ]

            error_msg = [
                    "\nNot an azair.eu search results link!",
                    "\nNot an english version of the site!",
                    "\nDoesn't include return flight!",
                    "\nOnly direct flights!"
            ]

            for i in range(len(requirements)):
                if not re.search(requirements[i], u):
                    print(error_msg[i])
                    return None

            return u

    def parse_results(self):
        page = requests.get(self.url).text
        soup = BeautifulSoup(page, "html.parser")
        results_data = soup.find("body", class_="results flexi").find("div", class_="list").find_all("div", class_="text")

        for element in results_data:
            cities_from_soup = element.p.find("span", class_="from")
            cities_to_soup = element.p.find("span", class_="to")
            codes_from_soup = element.p.find("span", class_="from").find("span", class_="code")
            codes_to_soup = element.p.find("span", class_="to").find("span", class_="code")
            dates_soup = element.p.find("span", class_="date")
            len_of_stay_soup = element.find("div", class_="totalPrice").find("span", class_="lengthOfStay")
            prices_soup = element.find_all("span", class_="subPrice")
            total_price_soup = element.find("div", class_="totalPrice").find("span", class_="tp")
            ids_soup = element.find_all("div", class_="detail")

            self.cities_from.append(f"{cities_from_soup.contents[1].strip()} ({codes_from_soup.contents[0]})")
            self.cities_to.append(
                f"{re.search(r'\d\d:\d\d (.+)', cities_to_soup.contents[0]).group(1)} ({codes_to_soup.contents[0]})")
            self.id_list.append(
                f'{ids_soup[0].p.find("span", class_="checked")["data-id"]}, {ids_soup[1].p.find("span", class_="checked")["data-id"]}')
            self.dates.append(dates_soup.text)
            self.len_of_stay_list.append(re.search(r"Length of stay: (\d\d? days)", len_of_stay_soup.text).group(1))
            self.there_price_list.append(prices_soup[0].text)
            self.back_price_list.append(prices_soup[1].text)
            self.total_price_list.append(total_price_soup.text)

    def print_parsed_results(self):
        df = pd.DataFrame(self.data_to_print)
        pd.set_option('display.colheader_justify', 'center')
        pd.set_option('display.max_rows', None)
        print("\n", df, "\n", sep="")

    def save_trip(self, i, saved_data_length):
        response_price_there = requests.get('https://api.azair.io/scrapfresh.php?id=' + self.id_list[i].split(ID_SPLITTER)[0]
                                            + '&apikey=d41d8cd98f00b204e9800998ecf8427e&cache=-1&format=json').json()
        response_price_back = requests.get(
            'https://api.azair.io/scrapfresh.php?id=' + self.id_list[i].split(ID_SPLITTER)[1]
            + '&apikey=d41d8cd98f00b204e9800998ecf8427e&cache=-1&format=json').json()
        c = CurrencyConverter()
        there_latest_date = response_price_there["valid"]
        there_currency = response_price_there["currency"]
        there_latest_price = round(c.convert(response_price_there["price"], there_currency, 'EUR'), 2)
        back_latest_date = response_price_back["valid"]
        back_currency = response_price_back["currency"]
        back_latest_price = round(c.convert(response_price_back["price"], back_currency, 'EUR'), 2)
        total_latest_price = round(there_latest_price + back_latest_price, 2)

        if there_latest_date > back_latest_date:
            max_latest_date = there_latest_date
        else:
            max_latest_date = back_latest_date

        with open(SAVED_DATA_PATH, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writerow(
                {
                    "id": self.id_list[i],
                    "date": self.dates[i],
                    "len_of_stay": self.len_of_stay_list[i],
                    "from": self.cities_from[i],
                    "to": self.cities_to[i],
                    "saved_total_price": total_latest_price,
                    "saved_there_price": there_latest_price,
                    "saved_back_price": back_latest_price,
                    "saved_total_price_date": max_latest_date
                }
            )
