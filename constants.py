SAVED_DATA_PATH = "Classes/saved_data/flights_data.csv"
ID_SPLITTER = ", "
UPDATED_PRICES_HEADERS = {
                "from": "From",
                "to": "To",
                "date": "Trip date",
                "len_of_stay": "Length of stay",
                "there_latest_price": "1st flight price",
                "there_price_change": "Change",
                "back_latest_price": "Return flight price",
                "back_price_change": "Change",
                "latest_price": "Total price",
                "latest_price_change": "Change",
                "total_price_date": "Latest price date"
}
QUESTION_INDEX_1 = "Enter the index of the trip you want to delete from followed, or [B] to get to the menu: "
QUESTION_MENU = "Chose [1] to execute a new search or [2] to exit the program: "
QUESTION_INDEX_3 = ("Enter the index of the trip to follow the prices of "
                    "its flights or [Q] to save the results and exit the program: ")
FIELDNAMES = ["id", "date", "len_of_stay", "from", "to", "total_price",
                            "there_price", "back_price", "total_price_date"]
REQUEST_LINE_1 = "https://api.azair.io/scrapfresh.php?id="
# The API key shown here is not mine, it is hardcoded into the web page, so I guess it's just the way the page
# handles price updates
REQUEST_LINE_2 = "&apikey=d41d8cd98f00b204e9800998ecf8427e&cache=-1&format=json"
MENU_CHOICES = [1, 2]
URL_INPUT_MSG = ("\nInput azair.eu search results meeting following requirements:\n"
                 "* Include return flight\n"
                 "* Only direct flights: ")
URL_REQUIREMENTS = [
                    r"^(?:https://|http://)?(www\.)?azair\.eu",
                    r"&isOneway=return&",
                    r"&maxChng=0&"
            ]
URL_ERR_MSG = [
                    "\nNot an azair.eu search results link!",
                    "\nDoesn't include return flight!",
                    "\nOnly direct flights!"
            ]
NEW_LINE = "\n"
EXIT_MSG = ("Thank you for using Flight Prices Updater. Updated prices of flights of newly "
            "saved trips should be added to the table at the start of the programme")
MENU_EXIT_MSG = "Thank you for using Flight Prices Updater. Have a nice day!"
