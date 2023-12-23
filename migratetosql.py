import pandas as pd
import sqlalchemy
import mysql.connector 
import sqlalchemy
import mongo
import ssl
import mysql.connector as sql 
from isodate import parse_duration
from dateutil.parser import isoparse
from datetime import datetime


def migrate_to_Sql(channelid):
# def main():

    db_connection = sql.connect(
        host="localhost",
        user="root",
        password="root",
        database="youtube"
    )
    # channel_id = "UCbzSATbuvVT5qMcOCNRMYnw"
    channel_id=channelid

    cursor = db_connection.cursor()

    migration_data = mongo.find_function(channel_id)

    if migration_data:
        query_channel = """
                INSERT INTO Channel (
                    channel_id,
                    channel_name,
                    Channel_subscription,
                    channel_views,
                    channel_description,
                    channel_status
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    """
        values_channel = (
                    migration_data['Channel_Name']['channel_id'],
                    migration_data['Channel_Name']['channel_name'],
                    migration_data['Channel_Name']['subscriber_count'],
                    migration_data['Channel_Name']['channel_views'],
                    migration_data['Channel_Name']['channel_description'],
                    "Active"
                )
        
        query_playlist = """
                INSERT INTO playlist (
                    playlist_id,
                    channel_id,
                    playlist_name
                    ) VALUES (%s, %s, %s)
                    """
        values_playlist = (
                    migration_data['Channel_Name']['playlist_id'],
                    migration_data['Channel_Name']['channel_id'],
                    "Vidoes"
                )

        
        cursor.execute(query_channel, values_channel)
        cursor.execute(query_playlist, values_playlist)

        video_data = migration_data.get("videos", {})

        for video_id, video_info in video_data.items():

            published_at_iso = video_info.get('published_at')
            published_at_datetime = datetime.fromisoformat(published_at_iso)
            published_at_formatted = published_at_datetime.strftime('%Y-%m-%d %H:%M:%S')
            query_video = """
                            INSERT INTO video (
                                video_id ,
                                playlist_id ,
                                video_name ,
                                video_description ,
                                published_at ,
                                view_count ,
                                like_count ,
                                dislike_count ,
                                favorite_count ,
                                comment_count ,
                                duration ,
                                thumbnail ,
                                caption_status
                                ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """
            values_video = (
                            video_info.get('video_id'),
                            migration_data['Channel_Name']['playlist_id'],
                            video_info.get('video_name'),
                            video_info.get('video_description'),
                            published_at_formatted,
                            video_info.get('view_count'),
                            video_info.get('like_count'),
                            video_info.get('dislike_count'),
                            video_info.get('favorite_count'),
                            video_info.get('comment_count'),
                            "10",
                            video_info.get('thumbnail'),    
                            video_info.get('caption_status')    
                        )
            cursor.execute(query_video, values_video)

        for video_id, video_info in video_data.items():
            comment_data = video_info.get('comments', {})
            videoid=video_info.get('video_id')
            query_Comment = """
                            INSERT INTO Comment (
                                comment_id,
                                video_id,
                                comment_text,
                                comment_author,
                                comment_published_at
                                )VALUES(%s,%s,%s,%s,%s)       
                        """
            
            if comment_data is not None:
                if isinstance(comment_data, list):
                    pass
                elif isinstance(comment_data, dict):
                    for comment_id, comment_info in comment_data.items():
                        published_at_comment = comment_info['comment_published_at']
                        published_at_datetime = datetime.fromisoformat(published_at_comment)
                        published_at_format = published_at_datetime.strftime('%Y-%m-%d %H:%M:%S')
                        values_comment = (
                            comment_info['comment_id'],
                            videoid,
                            comment_info['comment_text'],
                            comment_info['comment_author'],
                            published_at_format
                        )
                        cursor.execute(query_Comment, values_comment)
            
    db_connection.commit()   
    print("Data migrated successfully from MongoDB to MySQL data warehouse!")    
    return "Data migrated successfully from MongoDB to MySQL data warehouse!"

# if __name__ == "__main__":
#     main()