import get_videos
import get_bands

print('---- START ----')

# get videos from YouTube playlists
print('Getting videos from YouTube...')
df = get_videos.get_yt_likes()
videos = get_videos.write_videosheet(df)

if videos[0] == True:
	print(f'Step 1 SUCCESS: {videos[1]}')
else:
	print(f'Step 1 FAIL: {videos[1]}')


# get similar bands (execute script)
print('Getting similar bands from last.fm...')
bands = get_bands.get_bands()

if bands[0]==True:
	print(f'Step 2 SUCCESS: {bands[1]}')
else:
	print(f'Step 2 FAIL: {bands[1]}')

print('---- DONE ----')