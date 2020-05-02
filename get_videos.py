###### GET THE MUSIC VIDEOS FROM YOUTUBE AND SAVE TO GOOGLE SHEET ######

import config
from requests import get
import math
import pandas as pd
import gspread_pandas as gspd


def get_yt_likes(playlists=config.playlists,yt_key=config.yt_key,debug=0):
    
    ###### PARSE VIDEOS ######
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
    ###########################


    df = pd.DataFrame()
    baseurl = 'https://www.googleapis.com/youtube/v3/playlistItems?'

    for playlist in playlists:
        loops = 0
        params = 'part=snippet&maxResults=4&playlistId='+playlist+'&key='+yt_key
        
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
    


def write_videosheet(df,email=config.email,file=config.file,sheet_size=config.sheet_size,secret_file=config.secret_file,col_names=config.col_names,debug=0):
    df_work = pd.DataFrame(columns=col_names)
    df_sheet = pd.DataFrame()

    # open spread
    spread = gspd.spread.Spread(file, config=gspd.conf.get_config(file_name=secret_file), user=email)
    
    # loop through all the sheets and check if they are full and add content to df_work, create a new sheet if all are full and open it
    for index, sheet in enumerate(spread.sheets, start=1):
        rows = len(sheet.col_values(1))
        sheet_count = len(spread.sheets)
        if debug == 1:
            print(f'Sheet: {sheet}, {rows} rows in sheet')
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

    if debug == 1:
        print(f'using sheet "{spread.sheet.title}"')

    sheet = spread.sheet
    # merge dataframes to remove duplicates: df_work are videos from sheet, df are youtube likes
    df_work = df.append(df_work, ignore_index=True)
    # remove duplicates by video id
    df_work.drop_duplicates('id',keep=False,inplace=True)
    
    if debug == 1:
        print(df_work)

    # remove all rows that are already processed
    df_work = df_work[df_work['processed'].isnull()]
    

    # save headers if it's a new sheet
    start_row = len(sheet.col_values(1))+1
    if start_row == 1:
        headers=True
    else:
        headers=False

    if df_work.empty:
        return False, 'DataFrame is empty, no new videos found'

    # write to sheet
    try:
        spread.df_to_sheet(df_work,index=False,headers=headers,start=(start_row,1),sheet=sheet)
        return True, f'Data written to sheet "{sheet.title}"'
    except:
        return False, 'Error while writing sheet'
    


