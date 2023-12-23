import os
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors
import json
import mongo

def retrieve_main(channelId):
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyDzf5VFHkVb77cjl9PPaNSwZVX3ZTpsz4c"
    youtube = build(api_service_name, api_version, developerKey=api_key)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        # id="UCbzSATbuvVT5qMcOCNRMYnw"
        id = channelId
    )
    response = request.execute()
    channel_information = {}

    channel_information["Channel_Name"] = {
            'channel_id': response['items'][0]['id'],
            'channel_name': response['items'][0]['snippet']['title'],
            'channel_description': response['items'][0]['snippet']['description'],
            'subscriber_count': response['items'][0]['statistics']['subscriberCount'],
            'channel_views': response['items'][0]['statistics']['viewCount'],
            'playlist_id': response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        }
    channel_information['videos'] = {}
        
    

    playlist_id = channel_information['Channel_Name']["playlist_id"]
    next_page_token = None

    while True:
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            pageToken=next_page_token
        ).execute()

        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_response = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=video_id
            ).execute()

            try:
                comments_response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id
                ).execute()

                comments = {}

                for i, comment in enumerate(comments_response['items'], 1):
                    comment_id = comment['id']
                    comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                    comment_author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
                    comment_published_at = comment['snippet']['topLevelComment']['snippet']['publishedAt']

                    comments[f"comment_id_{i}"] = {
                        "comment_id": comment_id,
                        "comment_text": comment_text,
                        "comment_author": comment_author,
                        "comment_published_at": comment_published_at
                    }

            except googleapiclient.errors.HttpError as e:
                if 'commentsDisabled' in str(e):
                    comments = ["Comments are disabled for this video"]
                else:
                    raise

            if video_response['items']:
                video_information = {
                    "video_id": video_id,
                    "video_name": video_response['items'][0]['snippet']['title'] if 'title' in video_response['items'][0]['snippet'] else "Not Available",
                    "video_description": video_response['items'][0]['snippet']['description'],
                    "tags": ["example", "video"],
                    "published_at": video_response['items'][0]['snippet']['publishedAt'],
                    "view_count": video_response['items'][0]['statistics']['viewCount'] if 'viewCount' in video_response['items'][0]['statistics'] else "0",
                    "like_count": video_response['items'][0]['statistics']['likeCount'] if 'likeCount' in video_response['items'][0]['statistics'] else "0",
                    "dislike_count": video_response['items'][0]['statistics']['dislikeCount'] if 'dislikeCount' in video_response['items'][0]['statistics'] else "0",
                    "favorite_count": video_response['items'][0]['statistics']['favoriteCount'] if 'favoriteCount' in video_response['items'][0]['statistics'] else "0",
                    "comment_count": video_response['items'][0]['statistics']['commentCount'] if 'commentCount' in video_response['items'][0]['statistics'] else "0",
                    "duration": video_response['items'][0]['contentDetails']['duration'],
                    "thumbnail": video_response['items'][0]['snippet']['thumbnails']['default']['url'],
                    "caption_status": "Available",
                    "comments": comments
                }

                channel_information['videos'][f"video_id_{video_id}"] = video_information

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    # Convert the dictionary to a JSON string
    # result_json = json.dumps(channel_information, indent=2)
    # print(channel_information)
    # mongo.some_function()
    print("Data successfully fetched")
    return channel_information

# if __name__ == "__main__":
#     main()
