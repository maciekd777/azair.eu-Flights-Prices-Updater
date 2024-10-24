from currency_converter import CurrencyConverter
import requests
import csv
from colorama import Fore
from tabulate import tabulate
from constants import (UPDATED_PRICES_HEADERS, SAVED_DATA_PATH, ID_SPLITTER, FIELDNAMES,
                       REQUEST_LINE_1, REQUEST_LINE_2, NEW_LINE)


class PricesUpdater(object):
    data_to_print = []
    updated_data = []

    @classmethod
    def check_flights_data(cls, saved_trip):
        """
        Parse updated prices of flights of previously saved trip from the website and appends the data to
        updated_data list. The prices are found using ids of the saved flights and converted to euros through
        CurrencyConverter.
        :param saved_trip: Dictionary containing information about the saved flights, which prices are going to be
        updated.
        """
        flight_there_data, flight_back_data = (requests.get(
                REQUEST_LINE_1 + str(saved_trip["id"].split(ID_SPLITTER)[i]) + REQUEST_LINE_2).json() for i in range(2))

        c = CurrencyConverter()

        cls.updated_data.append({
            "id": saved_trip["id"],
            "date": saved_trip["date"],
            "len_of_stay": saved_trip["len_of_stay"],
            "from": saved_trip["from"],
            "to": saved_trip["to"],
            "total_price": round(c.convert(flight_there_data["price"], flight_there_data["currency"], 'PLN')
                                 + c.convert(flight_back_data["price"], flight_back_data["currency"], 'PLN'), 2),
            "there_price": round(c.convert(flight_there_data["price"], flight_there_data["currency"], 'PLN'), 2),
            "back_price": round(c.convert(flight_back_data["price"], flight_back_data["currency"], 'PLN'), 2),
            "total_price_date": cls.check_latest_date(flight_there_data["valid"], flight_back_data["valid"])
        })

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

    @classmethod
    def check_changes(cls, trip, i):
        """
        Calculates the difference between saved and newly parsed prices of flights of the trip, and appends specific
        data to data_to_print list.
        :param trip: Trip, which data is analyzed
        :param i: Index of the analyzed trip, at which it's saved (old) data is contained in the saved_data list in the
        main() function and at which it's updated data is contained in the updated_data list
        """
        total_price_change = round(cls.updated_data[i]["total_price"] - float(trip["total_price"]), 2)
        there_price_change = round(cls.updated_data[i]["there_price"] - float(trip["there_price"]), 2)
        back_price_change = round(cls.updated_data[i]["back_price"] - float(trip["back_price"]), 2)

        cls.data_to_print.append({
                        "from": trip["from"],
                        "to": trip["to"],
                        "date": trip["date"],
                        "len_of_stay": trip["len_of_stay"],
                        "there_latest_price": cls.color_price(cls.updated_data[i]["there_price"], there_price_change),
                        "there_price_change": cls.color_price(cls.updated_data[i]["there_price"], there_price_change,
                                                  data_to_color="price_change"),
                        "back_latest_price": cls.color_price(cls.updated_data[i]["back_price"], back_price_change),
                        "back_price_change": cls.color_price(cls.updated_data[i]["back_price"], back_price_change,
                                                             data_to_color="price_change"),
                        "latest_price": cls.color_price(cls.updated_data[i]["total_price"], total_price_change),
                        "latest_price_change": cls.color_price(cls.updated_data[i]["total_price"], total_price_change,
                                                               data_to_color="price_change"),
                        "total_price_date": cls.updated_data[i]["total_price_date"]
                    })

    @classmethod
    def color_price(cls, price, price_change, data_to_color="price"):
        """
        Colors the data in a way depending on the differences between newly parsed and saved (old) prices.
        :param price: Newly parsed price of the flight
        :param price_change: The difference between newly parsed and saved (old) price
        :param data_to_color: Indicates the data, which will be colored and returned. If it's equal to "price",
        function returns the colored price, otherwise returns the colored price_change
        :return: Colored price or price_change, depending on the data_to_color parameter
        """
        if price_change > 0:
            colored_price = f"{Fore.RED}↑ {price}{Fore.RESET}"
            colored_price_change = f"{Fore.RED}{price_change}{Fore.RESET}"
        elif price_change < 0:
            colored_price = f"{Fore.GREEN}↓ €{price}{Fore.RESET}"
            colored_price_change = f"{Fore.GREEN}{abs(price_change)}{Fore.RESET}"
        else:
            colored_price = price
            colored_price_change = price_change

        if data_to_color == "price":
            return colored_price
        else:
            return colored_price_change

    @classmethod
    def updated_prices_displayer(cls):
        """
        Prints the data from data_to_print in the form of pretty table, using tabulate module.
        """
        print(NEW_LINE, tabulate(cls.data_to_print, headers=UPDATED_PRICES_HEADERS, numalign="center",
                                 stralign="center", showindex=True), NEW_LINE)

    @classmethod
    def updated_prices_to_csv(cls):
        """
        Saves the new data from updated_data list to the CSV file.
        """
        with open(SAVED_DATA_PATH, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            for trip in cls.updated_data:
                writer.writerow(
                    {
                        "id": trip["id"],
                        "date": trip["date"],
                        "len_of_stay": trip["len_of_stay"],
                        "from": trip["from"],
                        "to": trip["to"],
                        "total_price": trip["total_price"],
                        "there_price": trip["there_price"],
                        "back_price": trip["back_price"],
                        "total_price_date": trip["total_price_date"]
                    }
                )

