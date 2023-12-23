import pandas as pd
import sqlalchemy
import mysql.connector as sql 

db_connection = sql.connect(
        host="localhost",
        user="root",
        password="root",
        database="youtube"
    )

def analysis_query(option):

    cursor = db_connection.cursor()

    if option == 1:
        cursor.execute(
                    """select c.channel_name, vp.video_name from channel c join (
                        select v.video_name,p.channel_id from video v join playlist p on v.playlist_id = p.playlist_id ) vp on 
                        c.channel_id = vp.channel_id""")
        result = cursor.fetchall()
        return result
    elif option == 2:
        cursor.execute(
                """select c.channel_name, count(vp.video_name) as video_count from channel c join (
                    select v.video_name,p.channel_id from video v join playlist p on v.playlist_id = p.playlist_id ) vp on 
                    c.channel_id = vp.channel_id group by c.channel_name""")
        result = cursor.fetchall()
        return result
    elif option == 3:
        cursor.execute(
                """select vp.video_name,c.channel_name,vp.view_count from channel c join (
                    select v.video_name,v.view_count,p.channel_id from video v join playlist p on v.playlist_id = p.playlist_id
                    order by view_count desc limit 10) vp on c.channel_id = vp.channel_id""")
        result = cursor.fetchall()
        return result
    elif option == 4:
        cursor.execute(
                """select vp.video_name,c.channel_name,vp.comment_count from channel c join (
                    select v.video_name,v.comment_count,p.channel_id from video v join playlist p on v.playlist_id = p.playlist_id
                    order by comment_count desc limit 10) vp on c.channel_id = vp.channel_id""")
        result = cursor.fetchall()
        return result
    elif option == 5:
        cursor.execute(
                """select vp.video_name,c.channel_name,vp.like_count from channel c join (
                    select v.video_name,v.like_count,p.channel_id from video v join playlist p on v.playlist_id = p.playlist_id
                    order by like_count desc limit 10) vp on c.channel_id = vp.channel_id""")
        result = cursor.fetchall()
        return result
    elif option == 6:
        cursor.execute(
                """select vp.video_name,vp.like_count from channel c join (
                    select v.video_name,v.like_count,p.channel_id from video v join playlist p on v.playlist_id = p.playlist_id
                    ) vp on c.channel_id = vp.channel_id""")
        result = cursor.fetchall()
        return result
    elif option == 7:
        cursor.execute(
                """select channel_name,channel_views from Channel""")
        result = cursor.fetchall()
        return result
    elif option == 8:
        cursor.execute(
                """select distinct(channel_name) from channel c join (
                    select p.channel_id from video v join playlist p on v.playlist_id = p.playlist_id 
                    where EXTRACT(YEAR FROM v.published_at) = 2022) vp on c.channel_id = vp.channel_id""")
        result = cursor.fetchall()
        return result
    elif option == 9:
        cursor.execute(
                """select c.channel_name,vp.avg_duration from channel c join (
                    select v.playlist_id , avg(v.duration) as avg_duration,p.channel_id from video v 
                    join playlist p on v.playlist_id = p.playlist_id
                    group by v.playlist_id,p.channel_id  ) vp on c.channel_id = vp.channel_id""")
        result = cursor.fetchall()
        return result
    elif option == 10:
        cursor.execute(
                """WITH RankedVideos AS (
                    select c.channel_id,c.channel_name,vp.video_name,vp.comment_count,vp.row_num from channel c join (
                    select v.video_name,v.comment_count,p.channel_id ,
                    ROW_NUMBER() OVER (PARTITION BY p.channel_id ORDER BY v.comment_count DESC) AS row_num
                    from video v join  playlist p on v.playlist_id = p.playlist_id ) vp on
                    c.channel_id = vp.channel_id )
                    SELECT channel_name,video_name,comment_count FROM RankedVideos WHERE row_num = 1""")
        result = cursor.fetchall()
        return result
    
def list_channel_names(): 
        cursor = db_connection.cursor()
        cursor.execute("select channel_name,channel_subscription,channel_views from channel")
        list_name = cursor.fetchall()
        return list_name  