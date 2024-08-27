import sys
from Classes.DataReader import DataReader
from Classes.PricesUpdater import PricesUpdater
from Classes.NewDataParser import NewDataParser
from constants import *


def main():
    data_reader = DataReader()
    data_reader.create_saved_data_list()
    remaining_data = data_reader.saved_data_list

    if len(remaining_data) > 0:
        prices_updater = PricesUpdater()
        prices_updater.prices_scraper(remaining_data)
        prices_updater.updated_prices_to_csv()
        prices_updater.updated_prices_displayer()

    while len(remaining_data) > 0:
        i = ask_for_index(QUESTION_INDEX_1, range(len(remaining_data)), "b")
        try:
            if del_index_from_list(remaining_data, i) == "y":
                data_reader.delete_trip(i)
                prices_updater.reset_lists()
                prices_updater.prices_scraper(remaining_data)
                prices_updater.updated_prices_to_csv()
                if len(remaining_data) > 0:
                    prices_updater.updated_prices_displayer()
        except TypeError:
            if i == "b":
                break

    menu = ask_for_index(QUESTION_INDEX_2, [1, 2], None)
    if menu == 2:
        sys.exit()

    parser = NewDataParser()
    while True:
        parser.url = parser.get_url()
        if parser.url:
            break

    parser.parse_results()
    parser.print_parsed_results()
    while True:
        save_index = ask_for_index(QUESTION_INDEX_3, range(len(parser.id_list)), "q")
        if save_index == "q":
            break
        elif any(trip["id"] == parser.id_list[save_index] for trip in data_reader.saved_data_list):
            print("\nTrip already followed!\n")
        else:
            parser.save_trip(save_index, len(data_reader.saved_data_list))
            data_reader.create_saved_data_list()


def ask_for_index(question, index_range, quit_char):
    while True:
        answer = input(question).strip().lower()
        if answer == quit_char:
            return answer

        try:
            answer = int(answer)
        except ValueError:
            print("\nIndex is not an integer!\n")
        else:
            if answer in index_range:
                return answer
            else:
                print("\nIndex out of range!\n")


def del_index_from_list(from_list, index):
    while True:
        answer = input(f"Are you sure you want to stop following the trip from {from_list[index]['from']} to "
                       f"{from_list[index]['to']}? Type [y] or [n]: ").strip().lower()
        if answer == "y" or answer == "n":
            return answer
        else:
            print("Wrong answer!")


if __name__ == "__main__":
    main()
