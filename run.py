import get_videos
import get_bands
import logging

logging.basicConfig(filename='similarbands.log', level=logging.INFO, format='%(levelname)s:%(name)s:%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)

message = f'---- START: {get_bands.timestamp} ----'
print(message)
log.info(message)

# get videos from YouTube playlists
message = f'Getting videos from YouTube...'
print(message)
log.info(message)

df = get_videos.get_yt_likes()
videos = get_videos.write_videosheet(df)

if videos[0] == True:
	message = f'Step 1 SUCCESS: {videos[1]}'
	print(message)
	log.info(message)
else:
	message = f'Step 1 FAIL: {videos[1]}'
	print(message)
	log.info(message)


# get similar bands (execute script)
message = 'Getting similar bands from last.fm...'
print(message)
log.info(message)

bands = get_bands.get_bands()

if bands[0]==True:
	message = f'Step 2 SUCCESS: {bands[1]}'
	print(message)
	log.info(message)
else:
	message = f'Step 2 FAIL: {bands[1]}'
	print(message)
	log.info(message)

message = '---- DONE ----'
print(message)
log.info(message)