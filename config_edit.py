email = '' # your email address (the one that's connected to your Google account with the API access)
file = '' # name of your Google Sheets file, e.g.: My_liked_videos
sheet_size = 20000 # max. no of rows after which a new sheet will be created (in the same file)
secret_file = '' # absolute path on your system to your google secrets file e.g.: /Users/user1/folder1/folder2/google_secret.json
lastfm_key = '' # your last.fm API key
playlists = [''] # the id's of the YouTube playlists you want to check (need to be public) in list format e.g.: ['1234567890','2345678901']
yt_key = '' # your YouTube API key
yt_baseurl = 'https://www.youtube.com/watch?v=' # base url for url column in sheet