# BFI Weekend Box Office Reporting

## Overview

* This project transforms the British Film Institute's weekend box office reports into interactive web-based applications using Dash.
* The existing reporting format for these weekly reports is Excel (`xls`). Each report contains:
  * A table with data about the top 15 films showing in the UK box office
  * A table with data about other UK films on release over the weekend *("other" meaning not in the top 15)*
  * A table with data about other new releases *("other" meaning not in the top 15 or UK tables)*
  * Comments/summary statistics relating to the top 15 results
  * On films where Previews have been take into account, explanatory notes regarding the weekend gross figures collected on these films
  * A table of titles opening in the box office next week
* All of these datasets and related facts are presented on a single sheet within an Excel file, and blank rows are used to separate the presentation of different datasets, making errors more likely if users attempt to manipulate the data using filtering or sorting techniques.
* For film researchers and analysts looking to automate ingestion of the weekly report data into their own pipelines, this is also not straightforward - automation scripts would need to be able to account for any small changes in layout, different capitalisation or punctuation in table headings.
* I engineered the beginning stages of a new web-app reporting format which presents the data found in the Excel file in a more intuitive way, and which lays the foundations for an end-user experience with greater flexibility and possibilities for interacting with, viewing, and downloading the data.
* The new layout gathers related but hitherto unlinked data from the Excel file, e.g.:
  * The notes on the individual films of the Top 15 table now occupy a **new "Notes" column** in the Top 15 table itself.
  * The user can now see **all UK films** in one table, regardless of whether they were in the top 15 or not in the top 15.
  * The user can now see **all new releases** in one table, regardless of whether they were in the top 15 or not in the top 15.
  * The **Openers Next Week** table has its own schema made up of just the columns that are relevant to it, rather than inheriting all the columns of the other tables above it on the Excel sheet.
* Additionally, the dashboard is engineered to display table views on the following subsets of data:
  * **UK films in the Top 15**
  * **New releases in the Top 15**
* The user has the option to select which subsection of data they want to view. (The next step in the implementation would be to provide users with the option to download the datasets they choose as csv or Excel files, ultimately with developed levels of customisation.)

## Technology stack
* **Languages:** Python
* **Key Frameworks:** Pandas (for data extraction and pre-processing), Dash (for building the web application)

## Installation instructions
* If getting the program running locally, open your terminal in a directory of your choosing and clone this repository:
```
$ git clone https://github.com/hillaabra/bfi-weekend-box-office-reports.git
```
* Get inside the directory and create a conda environment to install the required dependencies, e.g.:
```
cd bfi-weekend-box-office-reports
```
```
$ conda env create -f env.yaml -n boxoffice
```
* After activating the conda environment, run `app.py` on the command line with the pathway to the BFI weekend box office excel report of your choosing, e.g.:
```
$ python app.py xls_file_pathway.xls
```
* A message will be loaded to the command line telling you which http link Dash is running on, e.g. `http://127.0.0.1:8050/` - copy and paste this link to your browser of choice to view the app and start interacting with it.

## How it works
* The program begins by parsing the Excel file provided to it in the command-line argument using methods defined in the `excel_parser` module.
* Identified datasets, labels, column-names, and information, are read into pandas dataframes and saved as attributes of an `excel_parser` object.
* The program prepares the data for presentation on the dashboard:
  * Parsing and adding the addended notes to the table
  * Reformatting GBP currency values and percentage values for easier comprehension (using the methods defined in the `data_prepration` module)
* The program generates some new subsets of the tables and merges related datasets together as exlained above, so users can see all UK films in one place (whether coproduced with other territories or not), as well as all new releases.
* The `dash_styling` module contains functions to generate template Dash html and table components.
* The layout of the Dash app is defined in `app.py`, including a drop-down menu and callback visibility toggling function which enables the user to switch between datasets of their choosing.

## Why this adds value
* The additional subsets, merges and cohesion of related data points make for a more intuitive interaction with the data, whether the user's interest is in the top 15 performing films, all UK films, or all new or upcoming releases.
* The drop down-menu creates a user-driven interactive experience, since users to view different views or subsets of the data based on their specific needs.
* The new format lays a strong foundation for future enhancements to offer users greater flexibility with how they interact with, view, and download the data for analysis.

## How I would develop the app further
* Look at BFI's existing workflow for its creation of the Excel reports to assess how to access the source data before it is written to the xls file (for a more robust program).
* Implement downloading functionality using Dash Core Components - providing options for csv and Excel downloads, as well as to download multiple datasets, or all.
* Link a stylesheet - implement style from BFI Digital style bible.
* Implement better "total gross" UI - and implement it for all subsets of data so whatever subset is seen on the screen with the revenue columns, the total values are updated for the subset on view.
* Make the app a one-stop shop for all historic weekend box office reports - datasets across reports should be linked. Within the app, users should be able to filter for time periods and to click on a film and access data on its whole run without having to manually join datasets from separate reports.
* Continously work towards giving users more and more flexibility with how to access, view and download data - from filtering functionality (by country of origin, distributor, etc.) to interactive visualisations. (Implement one hot-encoding on the data for this.)
* Depending on budget, link relevant filmographical detail from e.g. IMDB's API, to help end-users contextualise the revenue data (e.g. language of the film (whether English-language or foreign), production budget where available, and genre).
* Continue refactoring the code and make it more modular.
* Continue testing the code and implementing more error handling.
* Set up scheduled automation so that the program runs every week.
* Ensure layout is responsive so that it can be used on different sized devices.
