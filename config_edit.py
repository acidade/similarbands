email = '' # your email address (the one that's connected to your Google account with the API access)
secret_file = '' # absolute path on your system to your google secrets file e.g.: /Users/user1/folder1/folder2/google_secret.json --> get it in the Google Console (https://console.developers.google.com)

file = '' # name of your Google Sheets file, e.g.: My_liked_videos
col_names = ['id','url','title','description','processed','band','similar1','similar1_link','similar2','similar2_link','similar3','similar3_link','similar4','similar4_link','similar5','similar5_link'] # change only if you know what you're doing
sheet_size = 20000 # max. no of rows after which a new sheet will be created (in the same file)

lastfm_key = '' # your last.fm API key

yt_key = '' # your YouTube API key --> get it in the Google Console (https://console.developers.google.com)
playlists = [''] # the id's of the YouTube playlists you want to check (need to be public) in list format e.g.: ['1234567890','2345678901']
yt_baseurl = 'https://www.youtube.com/watch?v=' # base url for url column in sheet