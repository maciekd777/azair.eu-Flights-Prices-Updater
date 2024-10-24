import sys
from Classes.DataReader import DataReader
from Classes.PricesUpdater import PricesUpdater
from Classes.NewDataParser import NewDataParser
from constants import QUESTION_INDEX_1, QUESTION_MENU, QUESTION_INDEX_3, MENU_CHOICES, NEW_LINE, EXIT_MSG, MENU_EXIT_MSG


def main():
    saved_data = DataReader.create_saved_data_list()

    if saved_data:
        print("Loading data...")
        for trip_index, trip in enumerate(saved_data):
            PricesUpdater.check_flights_data(trip)
            PricesUpdater.check_changes(trip, trip_index)
            PricesUpdater.updated_prices_to_csv()

    while saved_data:
        PricesUpdater.updated_prices_displayer()
        i = ask_for_index(QUESTION_INDEX_1, range(len(saved_data)), "b")
        if i == "b":
            break
        else:
            if _confirm_deletion(from_list=saved_data, index=i) == "y":
                _delete_trip(i)
                PricesUpdater.updated_prices_to_csv()

    menu()

    while True:
        NewDataParser.url = NewDataParser.get_url()
        if NewDataParser.url:
            break

    NewDataParser.parse_results()
    NewDataParser.print_parsed_results()
    while True:
        save_index = ask_for_index(QUESTION_INDEX_3, range(len(NewDataParser.id_list)), "q")
        if save_index == "q":
            sys.exit(EXIT_MSG)
        elif any(trip["id"] == NewDataParser.id_list[save_index] for trip in saved_data):
            print(NEW_LINE + "Trip already followed!" + NEW_LINE)
        else:
            NewDataParser.add_trip(save_index)
            DataReader.create_saved_data_list()


def ask_for_index(question, index_range, quit_char):
    """
    Asks for an integer corresponding to an index of the chosen element in the list and returns that index.
    :param question: Question asked
    :param index_range: Range of the list from which the user is choosing the element
    :param quit_char: Character that can be typed to leave the loop and end the choosing
    :return: Integer corresponding to an index of the chosen element or quit_char, if quit_char was specified
    """
    while True:
        answer = input(question).strip().lower()
        if answer == quit_char:
            return answer

        try:
            answer = int(answer)
        except ValueError:
            print(NEW_LINE + "Index is not an integer!" + NEW_LINE)
        else:
            if answer not in index_range:
                print(NEW_LINE + "Index out of range!" + NEW_LINE)
            else:
                return answer


def _confirm_deletion(from_list, index):
    """
    Asks for the confirmation of removing the element from the list.
    :param from_list: List, from which the element would be removed
    :param index: Integer corresponding to an index at which the element is in the list
    :return: Str "y" or "n" corresponding to "yes" (confirmation) and "no" (denial) of the deletion
    """
    while True:
        answer = input(f"Are you sure you want to stop following the trip from {from_list[index]['from']} to "
                       f"{from_list[index]['to']}? Type [y] or [n]: ").strip().lower()
        if not (answer == "y" or answer == "n"):
            print("Wrong answer!")
        else:
            return answer


def _delete_trip(index):
    """
    Deletes element from lists containing old and new data of previously saved trips.
    :param index: Index, at which the trip is contained in the lists
    """
    DataReader.saved_data_list.pop(index)
    PricesUpdater.data_to_print.pop(index)
    PricesUpdater.updated_data.pop(index)


def menu():
    """
    Ask via ask_for_index function to choose weather the user wants to execute the new search or exit the programme
    """
    print(NEW_LINE)
    if ask_for_index(QUESTION_MENU, MENU_CHOICES, 1) == 2:
        sys.exit(MENU_EXIT_MSG)


if __name__ == "__main__":
    main()
