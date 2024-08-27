SAVED_DATA_PATH = "Classes/saved_data/flights_data.csv"
ID_SPLITTER = ", "
UPDATED_PRICES_HEADERS = {
                "from": "From",
                "to": "To",
                "date": "Trip date",
                "len_of_stay": "Length of stay",
                "latest_price": "Latest total price",
                "latest_price_change": "Change",
                "there_latest_price": "1st flight latest price",
                "there_price_change": "Change",
                "back_latest_price": "Latest return flight price",
                "back_price_change": "Change",
                "latest_total_price_date": "Latest price date"
}
QUESTION_INDEX_1 = "Enter the index of the trip you want to delete from followed, or [B] to get to the menu: "
QUESTION_INDEX_2 = "Chose [1] to execute a new search or [2] to exit the program: "
QUESTION_INDEX_3 = "Enter the index of the trip to follow the prices of its flights or [Q] to save the results and exit the program: "
FIELDNAMES = ["id", "date", "len_of_stay", "from", "to", "saved_total_price",
                              "saved_there_price", "saved_back_price", "saved_total_price_date"]