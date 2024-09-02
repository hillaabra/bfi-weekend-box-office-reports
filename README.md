# BFI Weekend Box Office Reporting

## The Idea

* The BFI publishes weekly box office figures in Excel (`xls`) format every week. Each report contains:
  * A table with data about the top 15 films showing in the UK box office
  * A table with data about other (not in the top 15) UK films on release over the weekend
  * A table with data about other new releases (*"other" meaning not in the top 15 or UK tables*)
  * Comments/summary statistics relating to the top 15 results
  * On films where Previews have been take into account, explanatory notes regarding the weekend gross figures collected on these films
  * A table of titles opening in the box office next week
* All of these datasets and related facts are presented on a single sheet within an Excel file.
* I engineered the beginning stages of a new web-app reporting format which presents the data found in the Excel file in a more user-friendly way, with potential to give the end user more options for how they access and use the data.
* The new layout gathers related but hitherto unlinked data from the Excel file, e.g.:
  * The notes on the individual films of the Top 15 table now occupy a new "Notes" column.
  * The user can now see all the UK films in one table, regardless of whether they are in the top 15 or not in the top 15
  * The user can now see all the new releases in one table, regardless of whether they are in the top 15 or not in the top 15
  * The Openers Next Week table has its own schema made up of just the columns that are relevant to it, rather than inheriting all the columns of the other tables above it on the Excel sheet.
* Additionally, the dashboard is engineered to display table views on the following subsets of data:
  * UK films in the Top 15
  * New releases in the Top 15
* The user has the option to select which subsection of data they want to view. (The next step in the implementation would be to provide users with the option to download the datasets they choose as csv or excel files, ultimately with developed levels of customisation.)

## How it works

After cloning this repository, get inside the bfi-weekend-box-office-reports directory and run `app.py` with the BFI weekend box office excel report of your choosing, e.g.:
TODO: Add directory of xsl files to for testing.
```
python app.py xls_file_pathway
```
* The program begins by parsing the excel file provided to it in the command-line argument.
* Identified datasets, labels, and information, are read into pandas dataframes and saved as attributes of an `excel_parser` object.
* The program prepares the data for presentation on the dashboard:
  * Parsing and adding the addended notes to the table
  * Reformatting GBP currency values and percentage values for easier comprehension
* The program generates some new subsets of the tables and merges related datasets together as exlained above (so users can see all UK films in one place, as well as all new releases).
* The `dash_styling` module contains functions to generate Dash html and table components.
* The layout of the Dash app is defined in `app.py`, including a drop-down menu and callback visibility toggling function which enables the user to switch between datasets of their choosing.

## How it was built
* Programming languages: Python
* Python libraries:
  * pandas
  * dash
  * xlrd
  * re
  * math
  * argparse

## What value it adds


## How I would develop the app further
* Look at the existing workflow used to create the xls reports to see where code could be rewritten to become more robust, i.e. by accessing the source data before it is written to the xls file.
* Implement downloading functionality using Dash Core Components - providing options for csv and Excel downloads, as well as to download multiple datasets or all.
* Implement better "total revenue" UI - and implement it for all subsets of data so whatever subset is seen on the screen with the revenue columns, the total values are updated for the subset on view.
* Explore the existing BFI infrastructure for the long-term storage of weekly report relevant data.
* Make the app a one-stop shop for all historic weekend box office reports - datasets across reports should be linked. Within the app, users should be able to filter for time periods and to click on a film and access data on its whole run without having to manually join datasets from separate reports.
* Continously work towards giving users more and more flexibility with how to access, view and download data - from filtering functionality (by country of origin, distributor, etc.) to visualisations.
* Continue refactoring the code.
* Continue testing the code and implementing more error handling.
* Link a stylesheet - implement style from BFI Digital style bible.
* Automate process to run each week.