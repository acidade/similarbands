###### GET THE MUSIC VIDEOS FROM YOUTUBE AND SAVE TO GOOGLE SHEET ######

import config
from requests import get
import math
import pandas as pd

def get_yt_likes():
    loops = 0
    df = pd.DataFrame
    baseurl = 'https://www.googleapis.com/youtube/v3/playlistItems?'
    params = 'part=snippet&maxResults=4&playlistId='+config.playlist+'&key='+config.yt_key
    
    # get first page
    r = get(baseurl+params)
    response = r.json()
    page = 1
    df = parse_videos(page,df,response)

    # loop through all the pages
    loops = math.ceil(response['pageInfo']['totalResults']/response['pageInfo']['resultsPerPage'])
    for x in range(loops-1):
        r = get(baseurl+params+'&pageToken='+response['nextPageToken'])
        response = r.json()
        page = x+2
        df = parse_videos(page,df,response)
    return df
    

def parse_videos(page,df,response):
    print(f'Page {page}: {response}')
    #get id, url, title, description
    #put into df
    return df


def write_sheet(df):
    print('Placeholder (sheet written)')
    print(df)
    #open Spread
    #read sheets
    #compare sheets to df --> drop rows with duplicate id's from df
    #select last sheet
    #check if there are less than 1000-(df_rows) in sheet
        #if no, create new sheet
    #write df to sheet

df = get_yt_likes()
write_sheet(df)