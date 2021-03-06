###### GET VIDEOS FROM SHEET AND GET SIMILAR BANDS FROM LASTFM AND SAVE THEM TO SHEET ######

import config
import pandas as pd
import gspread_pandas as gspd
import time
import datetime
from requests import get
import logging
import urllib.parse

timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M')

logging.basicConfig(filename='similarbands.log', level=logging.INFO, format='%(levelname)s:%(name)s:%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)

###### READ and WRITE GOOGLE SHEET ######
def get_bands(email=config.email,file=config.file,secret_file=config.secret_file,timestamp=timestamp,debug=0):
	
	###### EXTRACT BANDNAME ######
	def extract_bandname(description):
		bandname = description.split(' - ')
		return bandname[0].strip()
	##############################

	###### CHECK LAST.FM ######
	def check_lastfm(bandname):
		similar_bands = {}
		bandname = urllib.parse.quote_plus(bandname)
		r = get('http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist='+bandname+'&api_key='+config.lastfm_key+'&format=json')
		jsonfile = r.json()
		try:
			for i in range(5):
				name = jsonfile['similarartists']['artist'][i]['name']
				url = jsonfile['similarartists']['artist'][i]['url']
				match = jsonfile['similarartists']['artist'][i]['match']
				similar_bands.update({name:{'url':url,'match':match}})
		except:
			similar_bands = {}
		return similar_bands
	###########################

	# open spread
	spread = gspd.spread.Spread(file, config=gspd.conf.get_config(file_name=secret_file), user=email)
	# loop through all the sheets in spread
	for sheet in spread.sheets:
		# load data from sheet to df
		df_work = spread.sheet_to_df(index=0, header_rows=1, start_row=1, sheet=sheet)  
		# loop through all the rows
		bands_checked = 0
		for index, row in df_work.iterrows():
			if row['processed'] == '':
				bands_checked += 1
				# extract bandname
				if row['band'] == '':
					bandname = extract_bandname(row['title'])
					df_work.at[index,'band'] = bandname			
				# check last.fm
				similar_bands = check_lastfm(row['band'])
				if similar_bands != {}:
					# write similar bands
					for band, name in enumerate(similar_bands, start=1):
						df_work.at[index,'similar'+str(band)] = name
						df_work.at[index,'similar'+str(band)+'_link'] = similar_bands[name]['url']
						df_work.at[index,'similar'+str(band)+'_match'] = similar_bands[name]['match']
				# write timestamp
				df_work.at[index,'processed'] = timestamp

		# print dataframe in debug mode
		if debug == 1:
			print(f'Sheet {sheet}:\n{df_work}')
		try:
			#save to sheet
			spread.df_to_sheet(df_work,index=False,sheet=sheet)
			return True, f'{bands_checked} bands checked. Similar bands written to sheet "{sheet.title}"'
		except:
			if debug == 1:
				print(f'FAIL: Could not write dataframe to sheet "{sheet}"')
			return False, f'Could not write similar bands to sheet "{sheet.title}"'






