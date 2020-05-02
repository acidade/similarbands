# Find similar bands

This script checks public YouTube playlists for videos and writes them to a Google Spreadsheet. It then tries to extract the artist name, looks for similar artists on last.fm and writes the top 5 similar artists back to the sheet.

### Installation

* Install all the Python dependencies in the requirements file: >> pip install -r requirements.txt
* Rename config_edit.py file to config.py and set all the variables
* See https://pypi.org/project/gspread-pandas/#client-credentials for more info on Google client credentials (secret_file variable, necessary for access to your spreadsheet)
* See https://www.last.fm/api/ for more info on last.fm API key
* Execute run.py

### Notes

At the moment this only works if the video titel contains only the artist name or data in the format "artist name - something something". The script is looking for " - " as separator after the artist name.

### Coming soon

Some analytics about number of artists, most recommended artists, etc.