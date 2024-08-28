from currency_converter import CurrencyConverter
import requests
import csv
from colorama import Fore
from tabulate import tabulate
from constants import UPDATED_PRICES_HEADERS, SAVED_DATA_PATH, ID_SPLITTER, FIELDNAMES


class PricesUpdater(object):
    def __init__(self):
        self.data_to_print = []
        self.updated_data_to_save = []

    def prices_scraper(self, saved_data):

        for trip in saved_data:

            response_price_there = requests.get(
                'https://api.azair.io/scrapfresh.php?id=' + str(trip["id"].split(ID_SPLITTER)[0])
                + '&apikey=d41d8cd98f00b204e9800998ecf8427e&cache=-1&format=json').json()
            response_price_back = requests.get(
                'https://api.azair.io/scrapfresh.php?id=' + str(str(trip["id"].split(ID_SPLITTER)[1]))
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

            there_price_change = round(there_latest_price - float(trip["saved_there_price"]), 2)
            back_price_change = round(back_latest_price - float(trip["saved_back_price"]), 2)
            total_price_change = round(total_latest_price - float(trip["saved_total_price"]), 2)

            if total_price_change > 0:
                total_price_c = f"{Fore.RED}↑ €{total_latest_price}{Fore.RESET}"
                total_price_change_c = f"{Fore.RED}+€{total_price_change}{Fore.RESET}"
            elif total_price_change < 0:
                total_price_c = f"{Fore.GREEN}↓ €{total_latest_price}{Fore.RESET}"
                total_price_change_c = f"{Fore.GREEN}-€{abs(total_price_change)}{Fore.RESET}"
            else:
                total_price_c = f"€{total_latest_price}"
                total_price_change_c = f"€{total_price_change}"

            if there_price_change > 0:
                there_price_c = f"{Fore.RED}↑ €{there_latest_price}{Fore.RESET}"
                there_price_change_c = f"{Fore.RED}+€{there_price_change}{Fore.RESET}"
            elif there_price_change < 0:
                there_price_c = f"{Fore.GREEN}↓ €{there_latest_price}{Fore.RESET}"
                there_price_change_c = f"{Fore.GREEN}-€{abs(there_price_change)}{Fore.RESET}"
            else:
                there_price_c = f"€{there_latest_price}"
                there_price_change_c = f"€{there_price_change}"

            if back_price_change > 0:
                back_price_c = f"{Fore.RED}↑ €{back_latest_price}{Fore.RESET}"
                back_price_change_c = f"{Fore.RED}+€{back_price_change}{Fore.RESET}"
            elif back_price_change < 0:
                back_price_c = f"{Fore.GREEN}↓ €{back_latest_price}{Fore.RESET}"
                back_price_change_c = f"{Fore.GREEN}-€{abs(back_price_change)}{Fore.RESET}"
            else:
                back_price_c = f"€{back_latest_price}"
                back_price_change_c = f"€{back_price_change}"

            self.data_to_print.append({
                        "from": trip["from"],
                        "to": trip["to"],
                        "date": trip["date"],
                        "len_of_stay": trip["len_of_stay"],
                        "latest_price": total_price_c,
                        "latest_price_change": total_price_change_c,
                        "there_latest_price": there_price_c,
                        "there_price_change": there_price_change_c,
                        "back_latest_price": back_price_c,
                        "back_price_change": back_price_change_c,
                        "latest_total_price_date": max_latest_date
                    })

            self.updated_data_to_save.append({
                        "id": trip["id"],
                        "date": trip["date"],
                        "len_of_stay": trip["len_of_stay"],
                        "from": trip["from"],
                        "to": trip["to"],
                        "saved_total_price": total_latest_price,
                        "saved_there_price": there_latest_price,
                        "saved_back_price": back_latest_price,
                        "saved_total_price_date": max_latest_date
                    })

    def updated_prices_displayer(self):
        print("\n", tabulate(self.data_to_print, headers=UPDATED_PRICES_HEADERS, numalign="center", stralign="center",
                             showindex=True), "\n")

    def updated_prices_to_csv(self):
        with open(SAVED_DATA_PATH, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            for trip in self.updated_data_to_save:
                writer.writerow(
                    {
                        "id": trip["id"],
                        "date": trip["date"],
                        "len_of_stay": trip["len_of_stay"],
                        "from": trip["from"],
                        "to": trip["to"],
                        "saved_total_price": trip["saved_total_price"],
                        "saved_there_price": trip["saved_there_price"],
                        "saved_back_price": trip["saved_back_price"],
                        "saved_total_price_date": trip["saved_total_price_date"]
                    }
                )

    def reset_lists(self):
        self.data_to_print = []
        self.updated_data_to_save = []
