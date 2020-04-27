# find similar bands

This script checks a Google Spreadsheet for new entries of YouTube videos. It reads the bands from this spreadsheet and checks via last.fm for similar bands. Similar bands are saved back to the spreadsheet.

### Installing

* Install all the dependencies in the requirements file.
* Rename config_edit.py file to config.py and define variables email (your email address with access to the Google Spreadsheet), file (the name of your google sheets file) and secret_file (full path location of your google secrets file, see https://pypi.org/project/gspread-pandas/ for more info)
* 