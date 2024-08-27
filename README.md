### Description
azair.eu is a website allowing to search for a cheap flights with various different options. This program is designed to scrap trips from azair.eu web search results, save those in which the user is interested in, and then check for updated prices for flights in those trips. Its behaviour can be split into the following actions:

#### Basic behaviour

* Print basic data of the saved trips, as well as updated prices of flights that are included in those trips, if any trip is saved
* Ask the user to input the index of the trip he is no longer interested in to delete the trip, or go back to the menu. The user is asked repeatedly for the input as long as he goes back to the menu, or there are no more trips to delete. The user is asked to reprompt the input if it wasn't an integer, or if the integer was out of range of the indexes.
* Ask the user if he wants to begin with new scraping to save another trip, or quit the program.
* If the user begins with the new scraping, he is asked for the url to azair.eu search results that includes trips he wants to save. The search should be done with the following options:
  * English version of the site
  * Return flights included, no one-way trips
  * Only direct flights
* If any of the above conditions is not satisfied, the user is asked to reprompt.
* If the url is ok, the program prints the table with every trip included in the search and asks the user to input the index of the trip he wants to save and follow it's prices, or to input Q to exit the program and save results. The user is asked repeatedly for the input until he enters Q.

#### Detailed behaviour

* Program starts with an infinite while loop, and firstly is trying to call the `get_saved_data` function, which reads the csv file `flights_data.csv` via `csv.DictReader`, then save the dictionaries of data in a list `l`, and then returns this list, which value is assign to the variable `saved_data` in the main function. If `saved_data` is successfully crested, the program continues on with creating two empty lists: `check_table` and `updated_prices`. Then, using the `requests` module and the data inside the `saved_data` list, the program is checking for the latest prices of flights included in the trip, which are automatically converted to euros thanks to the `currency_converter` module, and for the date of the latest price changes. Saved values are compared to scraped latest values and results are added to `check_table` for the user friendly table input (using colorama module), and then the latest values are appended to the `updated_prices` list, which is used to overwrite and update `flights_data.csv`. Then, the table is printed, using the `tabulate` module and data from the `check_table` list and the user is asked to either delete the trip entering its index, or go back to the menu by inputting B. The user is asked repeatedly for input (work of the while loop) as long as he enters B or there are no more trips to delete (program gets out of the loop). If the file doesn`t exist at the beginning, an empty list saved_data is created and the program gets out of the loop immediately.

<figure>
<img src="1.png" style="width:100%">
<center>Two saved trips from Katowice to Milan and the latest prices of the flights. In this example there is no difference between the prices scraped just after the program was run and the ones saved by the program after updating the prices last time</center>
</figure>


<figure>
<img src="2.png" style="width:100%">
<center>The same trips, but with manually changed saved prices, just to show how the program reacts to the prices changes. The latest price of the flight from Katowice to Milan ("1st flight") of the trip indexed "0" is 6 euros less compared to its saved price in the file, however the latest price of the flight from Milan to Katowice ("return flight") is 8 euros bigger compared to its saved price. As a result, the latest total price is now 2 euros bigger compared to the price saved by the program the last time</center>
</figure>


* After getting out from the while loop, the program is printing the "menu", which isn't actually a menu, it's just a choice between starting new scraping or exiting the program via `sys.exit`. To get the correct input, the `menu` function is called, which returns `True`, if the input matches the requirements, namely when user inputs `1` or `2`.

<figure>
<img src="3.png" style="width:100%">
<center>After inputing `B` the program prints out the "menu" where it's asking the user to start new search or exit the program</center>
</figure>

* If the user wants to start a new scraping, the function `get_url` is called, which asks the user to input azair.eu search result URL, and returns `True` if user input matches the requirements, namely:
  * The website must be in english
  * Return flights included, no one-way trips
  * Only direct flights

The first requirement is needed to match regular expression used to create `len_of_stay_list`, and the other ones are making sure that search results don`t have too many or too few flights.


<figure>
<img src="4.png" style="width:100%">
<center>The program asking the user to reprompt two times after two wrong inputs, "car", and an azair.eu search results URL, but with "max changes" option equal to 1, not to 0 (direct flights requirement not met)</center>
</figure>

* After inputting the correct URL, the function `get_lists` is called and it's taking the URL as an argument. Then, using the `beautifulsoup4` module, specific data from the web page is scraped and appended to one of the lists: `cities_from`, `cities_to`, `id_list`, `dates`, `len_of_stay_list`, `there_price_list`, `back_price_list`, `total_price_list`. After scraping, all lists are returned to the main function and assigned to variables there.

* Right after calling `get_lists` function there are two object created: `print_data` dictionary, and `all_data` list. The first one is created from some lists returned by `get_lists` function and it's purpose is to include only this data from results that is relevant to printing (for example flights IDs are not really relevant), and the second one is created from all lists returned by `get_lists` function. Further into the program `all_data` list is used to extract data necessary to save flights data to the file.

* When lists are created, the program is using the `pandas` module to create `DataFrame` object from `print_data` dictionary and printing it.

<figure>
<img src="5.png" style="width:100%">
<center>Printed table with search results of the correct link</center>
</figure>

* After printing the table, the `get_new_data` function is called with the `all_data` list taken as an argument. Inside this function there is an infinite while loop that asks the user for the index of the trip he wants to saved to the file and follow it's prices. Program asks the user to reprompt if the input is not integer or if the integer is out of range of the indexes. After inputting any correct index, the program is appending scraped latest data regarding the chosen trip to `data_list` list (this part of `get_new_data` function is similar to the scraping of the latest data at the beginning of the `main` function). Loop breaks when the user inputs `Q`. The `data_list` is returned and assigned to the `new_data_to_save` variable

<figure>
<img src="6.png" style="width:100%">
<center>The user has chosen to follow the flight prices of the trip indexed 9 and did exit the program</center>
</figure>

* At the end of the program, the function `save_data` is called and it takes two arguments: `new_data_to_save` and `saved_data`. The function uses the `csv` module to save `new_data_to_save` data to the `flights_data.csv` file, but only if the trip is not already saved in the file (program checks if the combination of IDs of the flights included in the chosen trip is not in the `saved_data` list, which was created from reading `flights_data.csv`. If the trip is in the list, instead of appending it to the file, program prints that this trip is already followed.

<figure>
<img src="7.png" style="width:100%">
<center>When running the program now, the trip recently added to following shows in the table and the prices of its flights are updated (total price in the table can differ a little bit from the total price shown in the search result, because scraped prices sometimes needs to be converted into euros from various other currencies)</center>
</figure>
