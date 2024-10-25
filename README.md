
# Flights Prices Updater

<div align="center">
<img src="https://github.com/user-attachments/assets/282f4003-166b-4300-8ac9-7becb0edf8d8">
</div>

Do you like exploring the world with budget airlines and keep looking for a bargain to buy a flight ticket? With help of Flights Prices Updater you can easily track changes of the flights found on azair.eu - popular website to look for budget flights opportunities.

## Authors

- [@maciekd777](https://github.com/maciekd777)


## Tech Stack

**Data preparation:** BeautifulSoup

**Data manipulation:** Pandas

## Installation

Get the source code and assets from github. Then, install requirements from requirements.txt.

```bash
git clone https://github.com/maciekd777/azair.eu-Flights-Prices-Updater.git
python -m pip install -r requirements.txt
python main.py
```

## Basic behavior

* Prints basic data of the saved trips with updated prices of flights that are included in those trips, if any trip is saved
* Asks the user to delete the trip by inputing the index of the trip he is no longer interested in, or go to the menu. The user is asked repeatedly for the input as long as he goes back to the menu, or there are no more trips to delete. The user is asked to reinput if the input wasn't an integer, or if the integer was out of range of the indexes
* Asks the user to begin with new scraping and save another trip, or quit the programme
* If the user begins with the new scraping, he is asked for the url to azair.eu search results that includes trips he wants to save. The search should be done with the following options:
  * Return flights included, no one-way trips
  * Only direct flights, no changes
* If any of the above conditions is not satisfied, the user is asked to reinput.
* If the url is ok, the programme prints the table with every trip included in the search and asks the user to input the index of the trip he wants to save and follow it's prices, or to input Q to exit the program and save the results. The user is asked repeatedly for the input until he enters Q.

Note that:
* **The programme has been tested only on english and polish version of the azair.eu website. Other languages are not promised to work**
* **The prices are saved in polish złoty (PLN). If you want to save prices in other currency, change the code in the following way:**

In the `PricesUpdater.py` find `check_flights_data` method, At the end of its body there should be this code:

```
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
```
and change all the 'PLN' strings to strings corresponding to the ISO code of the desired currency. The codes can be found on Wikipedia https://en.wikipedia.org/wiki/ISO_4217#List_of_ISO_4217_currency_codes.
Then, in the same way you need to change the code

```
there_price = round(c.convert(response_price_there["price"], response_price_there["currency"], 'PLN'), 2)
back_price = round(c.convert(response_price_back["price"], response_price_back["currency"], 'PLN'), 2)
```
at the begginning of the `add_trip` method in the `NewDataParser.py` file. At last, you need to change the code in the `color_price` method in the `PricesUpdater.py` file:

```
        if price_change > 0:
            colored_price = f"{Fore.RED}↑ {price} zł{Fore.RESET}"
            colored_price_change = f"{Fore.RED}{price_change} zł{Fore.RESET}"
        elif price_change < 0:
            colored_price = f"{Fore.GREEN}↓ {price} zł{Fore.RESET}"
            colored_price_change = f"{Fore.GREEN}{abs(price_change)} zł{Fore.RESET}"
        else:
            colored_price = f"{price} zł"
            colored_price_change = f"{price_change} zł"
```
Here prices and the difference in prices are changed to the 'currency format'. For polish złoty the price is written like "123 zł", so after the prices there is string " zł" added at the end. You can edit this to the format of the desired currency or delete " zł" after all `{price}`
and `{price_change}` to display only floats. For example, the code above for euros would look like this:
```
        if price_change > 0:
            colored_price = f"{Fore.RED}↑ €{price}{Fore.RESET}"
            colored_price_change = f"{Fore.RED}€{price_change}{Fore.RESET}"
        elif price_change < 0:
            colored_price = f"{Fore.GREEN}↓ €{price}{Fore.RESET}"
            colored_price_change = f"{Fore.GREEN}€{abs(price_change)}{Fore.RESET}"
        else:
            colored_price = f"€{price}"
            colored_price_change = f"€{price_change}"
```


## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

