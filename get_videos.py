###### GET THE MUSIC VIDEOS FROM YOUTUBE AND SAVE TO GOOGLE SHEET ######

import config
from requests import get
import math
import pandas as pd
import gspread_pandas as gspd


def get_yt_likes():
    
    df = pd.DataFrame()
    baseurl = 'https://www.googleapis.com/youtube/v3/playlistItems?'

    for playlist in config.playlist:
        loops = 0
        params = 'part=snippet&maxResults=4&playlistId='+playlist+'&key='+config.yt_key
        
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
    # loop through all videos
    for item in response['items']:        
        
        #put id, title, description into df

        video_id = item['snippet']['resourceId']['videoId']
        video_url = config.yt_baseurl + item['snippet']['resourceId']['videoId']
        video_title = item['snippet']['title']
        video_description = item['snippet']['description']

        df_video = pd.DataFrame.from_dict({'id':[video_id], 'url':[video_url], 'title':[video_title], 'description':[video_description]})
        df = df.append(df_video, ignore_index=True)
    
    return df


def write_sheet(df,email,file,sheet_size,secret_file):
    df_work = pd.DataFrame()
    df_sheet = pd.DataFrame()

    # open spread
    spread = gspd.spread.Spread(file, config=gspd.conf.get_config(file_name=secret_file), user=email)
    
    # loop through all the sheets and check if they are full and add content to df_work, create a new sheet if all are full and open it
    for index, sheet in enumerate(spread.sheets, start=1):
        rows = len(sheet.col_values(1))
        sheet_count = len(spread.sheets)
        print(f'Sheet: {sheet}, {rows} rows') # --> delete later
        # if sheet is full but not last sheet
        if rows >= sheet_size and index < sheet_count:
            df_sheet = spread.sheet_to_df(index=0, header_rows=1, start_row=1, sheet=sheet)
            df_work = df_work.append(df_sheet, ignore_index=True)
            continue
        # if sheet is full and is last sheet
        elif rows >= sheet_size and index == sheet_count:
            df_sheet = spread.sheet_to_df(index=0, header_rows=1, start_row=1, sheet=sheet)
            df_work = df_work.append(df_sheet, ignore_index=True)
            # create a new sheet
            sheet_title = f'Sheet{index+1}'
            spread.create_sheet(sheet_title,rows=1000,cols=20)
            spread.open_sheet(sheet_title, create=False)
            break
        else:
            # if not full, use this one
            df_sheet = spread.sheet_to_df(index=0, header_rows=1, start_row=1, sheet=sheet)
            df_work = df_work.append(df_sheet, ignore_index=True)
            spread.open_sheet(sheet.title, create=False)

    print(f'arbeiten mit "{spread.sheet.title}"') # --> delete later
    sheet = spread.sheet
    # merge dataframes to remove duplicates: df_work are videos from sheet, df are youtube likes
    df_work = df.append(df_work, ignore_index=True)
    # remove duplicates by video id
    df_work.drop_duplicates('id',keep=False,inplace=True)
    print(df_work)
    # remove all rows that are already processed
    df_work = df_work[df_work['processed'].isnull()]
    

    # save to sheet
    start_row = len(sheet.col_values(1))+1
    if start_row == 1:
        headers=True
    else:
        headers=False

    try:
        spread.df_to_sheet(df_work,index=False,headers=headers,start=(start_row,1),sheet=sheet)
        print('written to sheet') # --> delete later
        return True
    except:
        print(f'FAIL: Could not write dataframe to sheet "{sheet}"') # --> delete later
        return False
    

df = get_yt_likes()
write_sheet(df,config.email,config.file,config.sheet_size,config.secret_file)

