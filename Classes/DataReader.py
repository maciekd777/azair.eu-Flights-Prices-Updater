import csv
from constants import SAVED_DATA_PATH, FIELDNAMES


class DataReader(object):
    def __init__(self):
        self.saved_data_list = []

    def create_saved_data_list(self):
        try:
            with open(SAVED_DATA_PATH) as file:
                reader = csv.DictReader(file)
                for flight in reader:
                    self.saved_data_list.append({
                        "id": flight["id"],
                        "date": flight["date"],
                        "len_of_stay": flight["len_of_stay"],
                        "from": flight["from"],
                        "to": flight["to"],
                        "saved_total_price": flight["saved_total_price"],
                        "saved_there_price": flight["saved_there_price"],
                        "saved_back_price": flight["saved_back_price"],
                        "saved_total_price_date": flight["saved_total_price_date"]
                    })
        except FileNotFoundError:
            with open(SAVED_DATA_PATH, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()

    def delete_trip(self, index):
        self.saved_data_list.pop(index)
