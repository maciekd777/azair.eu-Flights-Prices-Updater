import csv
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from constants import (ID_SPLITTER, SAVED_DATA_PATH, FIELDNAMES, URL_REQUIREMENTS, URL_ERR_MSG,
                       URL_INPUT_MSG, NEW_LINE, REQUEST_LINE_1, REQUEST_LINE_2)
from currency_converter import CurrencyConverter


class NewDataParser:
    url = None
    cities_from_list = []
    cities_to_list = []
    id_list = []
    dates_list = []
    len_of_stay_list = []
    there_price_list = []
    back_price_list = []
    total_price_list = []
    data_to_print = {
            "From": cities_from_list,
            "To": cities_to_list,
            "Date": dates_list,
            "Length of stay": len_of_stay_list,
            "Total price": total_price_list
        }
    data_to_save = []

    @classmethod
    def get_url(cls):
        """
        Asks for the URL of the azair.eu search results from which the user wants to save a trip and track the prices
        of its flights. For the URL to meet the requirements the webpage should be in english, the trips should have
        there and return flights, and the flights should be direct only. The requirements are checked using re.search()
        function on the patterns from URL_REQUIREMENTS list, and if the pattern indexed "i" is not found, the message
        indexed "i" from the list URL_ERR_MSG is shown, and the function returns None. If every pattern is found, the
        function returns the URL typed.
        :return: URL typed by the user if it met all the requirements. If not, returns None.
        """
        while True:
            u = input(URL_INPUT_MSG)
            for i in range(len(URL_REQUIREMENTS)):
                if not re.search(URL_REQUIREMENTS[i], u):
                    print(URL_ERR_MSG[i])
                    return None
            return u

    @classmethod
    def parse_results(cls):
        """
        Fills all the lists in NewDataParser class with data parsed from the website using URL typed by the user.
        """
        page = requests.get(cls.url).text
        soup = BeautifulSoup(page, "html.parser")
        results_data = soup.find("body", class_="results flexi").find("div", class_="list").find_all("div", class_="text")

        for element in results_data:
            cities_from_list_soup = element.p.find("span", class_="from")
            cities_to_list_soup = element.p.find("span", class_="to")
            codes_from_soup = element.p.find("span", class_="from").find("span", class_="code")
            codes_to_soup = element.p.find("span", class_="to").find("span", class_="code")
            dates_list_soup = element.p.find("span", class_="date")
            len_of_stay_soup = element.find("div", class_="totalPrice").find("span", class_="lengthOfStay")
            prices_soup = element.find_all("span", class_="subPrice")
            total_price_soup = element.find("div", class_="totalPrice").find("span", class_="tp")
            ids_soup = element.find_all("div", class_="detail")

            cls.cities_from_list.append(f"{cities_from_list_soup.contents[1].strip()} ({codes_from_soup.contents[0]})")
            cls.cities_to_list.append(
                f"{re.search(r'\d\d:\d\d (.+)', cities_to_list_soup.contents[0]).group(1)} ({codes_to_soup.contents[0]})")
            cls.id_list.append(
                f'{ids_soup[0].p.find("span", class_="checked")["data-id"]}, {ids_soup[1].p.find("span", class_="checked")["data-id"]}')
            cls.dates_list.append(dates_list_soup.text)
            cls.len_of_stay_list.append(re.search(r".+: (\d\d?) ?.+", len_of_stay_soup.text).group(1) + " days")
            cls.there_price_list.append(prices_soup[0].text)
            cls.back_price_list.append(prices_soup[1].text)
            cls.total_price_list.append(total_price_soup.text)

    @classmethod
    def print_parsed_results(cls):
        """
        Prints parsed data in a tabular form using Pandas.
        """
        df = pd.DataFrame(cls.data_to_print)
        pd.set_option('display.colheader_justify', 'center')
        pd.set_option('display.max_rows', None)
        print(NEW_LINE, df, NEW_LINE, sep="")

    @classmethod
    def add_trip(cls, i):
        """
        Updates prices and appends the data of the trip indexed "i" from parsed results to the CSV file.
        :param i: Index at which the trip showed in the results table.
        """
        response_price_there = requests.get(REQUEST_LINE_1 + cls.id_list[i].split(ID_SPLITTER)[0] + REQUEST_LINE_2).json()
        response_price_back = requests.get(REQUEST_LINE_1 + cls.id_list[i].split(ID_SPLITTER)[1] + REQUEST_LINE_2).json()
        c = CurrencyConverter()
        there_price = round(c.convert(response_price_there["price"], response_price_there["currency"], 'PLN'), 2)
        back_price = round(c.convert(response_price_back["price"], response_price_back["currency"], 'PLN'), 2)
        total_price = round(there_price + back_price, 2)

        with open(SAVED_DATA_PATH, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writerow(
                {
                    "id": cls.id_list[i],
                    "date": cls.dates_list[i],
                    "len_of_stay": cls.len_of_stay_list[i],
                    "from": cls.cities_from_list[i],
                    "to": cls.cities_to_list[i],
                    "total_price": total_price,
                    "there_price": there_price,
                    "back_price": back_price,
                    "total_price_date": cls.check_latest_date(response_price_there["valid"], response_price_back["valid"])
                }
            )

    @classmethod
    def check_latest_date(cls, there_date, back_date):
        """
        Compares the dates of the latest prices of there and return flights, and returns the latest one.
        :param there_date: The date of the last change in the price of "there" flight (the first flight)
        :param back_date: The date of the last change in the price of the return flight
        :return: The latest date from there_date and back_date
        """
        if there_date > back_date:
            latest_date = there_date
        else:
            latest_date = back_date
        return latest_date

