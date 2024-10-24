import csv
from constants import SAVED_DATA_PATH, FIELDNAMES


class DataReader(object):
    saved_data_list = []

    @classmethod
    def create_saved_data_list(cls):
        """
        Reads the CSV file containing the data of previously saved flights, appends it to the saved_data_list list, and
        returns it. If the file does not exist, it is created with only header.
        :return: List of dictionaries containing data of the previously saved trips
        """
        try:
            with open(SAVED_DATA_PATH) as file:
                reader = csv.DictReader(file)
                for flight in reader:
                    cls.saved_data_list.append({
                        "id": flight["id"],
                        "date": flight["date"],
                        "len_of_stay": flight["len_of_stay"],
                        "from": flight["from"],
                        "to": flight["to"],
                        "total_price": flight["total_price"],
                        "there_price": flight["there_price"],
                        "back_price": flight["back_price"],
                        "total_price_date": flight["total_price_date"]
                    })

        except FileNotFoundError:
            with open(SAVED_DATA_PATH, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()

        return cls.saved_data_list
