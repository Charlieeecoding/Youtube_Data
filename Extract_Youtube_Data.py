# Extract NFL channel data by calling Youtube API 
print()
print('Youtube API project starts now...')

from googleapiclient.discovery import build 
from googleapiclient.errors import HttpError
import csv
import os.path
import time 
from datetime import datetime

print('Programme starts now')
start_time = time.perf_counter()
print()

# API information
api_service_name = "youtube"
api_version = "v3"
api_key = '<YOUR_YOUTUBE_API_KEY>'

# API client
youtube = build(api_service_name, api_version, developerKey = api_key)

# NFL Channel ID 
# channel_id = 'UCDVYQ4Zhbm3S2dlz7P1GBDg'


print('Now request Youtube for Channel information')
print('...')

# get channel id by using the youtube channel name - NFL
def get_channel_id(youtube):
    request = youtube.channels().list(
        part='id', 
        forUsername='NFL'
    )

    response = request.execute()

    return response['items']

channel_id = get_channel_id(youtube)

channel_id = channel_id[0]['id']

print(f"NFL's playlist ID is '{channel_id}'")


# Request for the first view about the YouTube channel - NFL
def get_channel_info_to_csv(youtube, channel_id, info_csv_file):
    request = youtube.channels().list(
        part='id, contentDetails, snippet, statistics',
        id=channel_id
    )

    # Request execution
    response = request.execute()
    channel_info = response['items'][0]  # Use index [0] to access the first item
    
    # Saving NFL channel information to the CSV file
    
    print('Saving informaiton to csv file...')
    print()

    csv_columns = ['CHANNEL_NAME', 'CHANNEL_ID', 'PUBLISHED_AT', 'SUBSCRIBER_COUNT', 'VIDEO_COUNT', 'VIEW_COUNT', 'DESCRIPTION', 'LOG_TIME']

    file_exists = os.path.isfile(info_csv_file)

    with open(info_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()

        writer.writerow({
            'CHANNEL_NAME':         str(channel_info['snippet']['title']),
            'CHANNEL_ID':           str(channel_info['id']),
            'PUBLISHED_AT':         str(channel_info['snippet']['publishedAt']),
            'SUBSCRIBER_COUNT':     str(channel_info['statistics']['subscriberCount']),
            'VIDEO_COUNT':          str(channel_info['statistics']['videoCount']),
            'VIEW_COUNT':           str(channel_info['statistics']['viewCount']),
            'DESCRIPTION':          str(channel_info['snippet']['description']), 
            'LOG_TIME':             datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return response['items'][0]  # Use index [0] to access the first item


info_csv_file = 'channel_information.csv'

channel_info = get_channel_info_to_csv(youtube, channel_id, info_csv_file)


# getting all playlist IDs from NFL channel, and save into csv file
def save_playlists_to_csv(playlist_ids, playlist_filename):
    with open(playlist_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['PLAYLIST_ID', 'TITLE', 'PUBLISH_DATE', 'ITEM_COUNT'])
        writer.writeheader()
        writer.writerows(playlist_ids)

def get_youtube_playlists(api_key, channel_id):

    youtube = build('youtube', 'v3', developerKey=api_key)

    print('Now getting all playlist IDs from NFL channel...')
    print()

    try:
        playlists = []
        next_page_token = None

        while True:
            playlists_response = youtube.playlists().list(
                part='id,snippet,contentDetails',
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for playlist in playlists_response['items']:
                playlist_id = playlist['id']
                playlist_title = playlist['snippet']['title']
                playlist_publish_date = playlist['snippet']['publishedAt']
                playlist_item_count = playlist['contentDetails']['itemCount']

                playlist_data = {
                    'PLAYLIST_ID': playlist_id,
                    'TITLE': playlist_title,
                    'PUBLISH_DATE': playlist_publish_date,
                    'ITEM_COUNT': playlist_item_count
                }

                playlists.append(playlist_data)

            next_page_token = playlists_response.get('nextPageToken')

            if not next_page_token:
                break

        if not playlists:
            return []

        return playlists

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        return []


playlist_ids = get_youtube_playlists(api_key, channel_id)

playlist_filename = 'playlists_information.csv'

save_playlists_to_csv(playlist_ids, playlist_filename)


print(f'Total there are {len(playlist_ids)} playlists')
print()


print('Opening all playlists to get all videos...')
print()


# Get all videos from all playlist IDs 
def get_playlist_videos(youtube, playlist_id):
    
    try:
        videos = []
        next_page_token = None

        while True:
            playlist_items_response = youtube.playlistItems().list(
                part='id,snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in playlist_items_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                playlist_id = item['snippet']['playlistId']
                video_title = item['snippet']['title']
                video_publish_date = item['snippet']['publishedAt']
                video_description = item['snippet']['description']

                video_data = {
                    'VIDEO_ID': video_id,
                    'PLAYLIST_ID': playlist_id,
                    'TITLE': video_title,
                    'PUBLISH_DATE': video_publish_date,
                    'DESCRIPTION': video_description
                }

                videos.append(video_data)

            next_page_token = playlist_items_response.get('nextPageToken')

            if not next_page_token:
                break

        if not videos:
            return []

        return videos

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        return []


# Save all videos from all playlist IDs into csv file
def save_videos_to_csv(all_videos, video_filename):
    with open(video_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['VIDEO_ID', 'PLAYLIST_ID', 'TITLE', 'PUBLISH_DATE', 'DESCRIPTION'])
        writer.writeheader()
        writer.writerows(all_videos)


video_filename = 'videos_information.csv'


total_playlist = len(playlist_ids)
playlist_count = 0
all_videos = []

for playlist in playlist_ids:
    playlist_count += 1
    videos = get_playlist_videos(youtube, playlist['Playlist ID'])
    print(f'{playlist_count}/{total_playlist} playlists have been processed')

    # Not all playlist has videos in it
    if videos:
        all_videos.extend(videos)
    else:
        print('No videos in this playlist')

save_videos_to_csv(all_videos, video_filename)


print('All information has been captured')
print()

end_time = time.perf_counter()
print(f'[{datetime.now().strftime("%b %d, %Y %H:%M:%S")}] The program total loading time is {end_time - start_time:0.1f} seconds')

exit_program = input('Please click Enter to exit')
