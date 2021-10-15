import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "11130780232"  # your Spotify username
TOKEN = "BQBKM9us_Rl0AGpqChXNh4kbStI-xF-v-DbNnEkfxRBM-NV6JtensIT4C0NWAnyM7hrs-JxIxvul3ypXWEg5Yfe1aN-G3RKW05D1BCycia2MRp9GGlSfyC6AlJvKYOkDivja4cIQ6PEF6sNl4hBREQ"  # your Spotify API token


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # check if dataframe is empty
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False
    # primary key constraint
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key Check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null value found")

    # check that all timestamps are of yesterday's date
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0,minute=0,second=0,microsecond=0)

    timestamps = df['timestamp'].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
            raise Exception("At least one of the returned songs does no come from within the last 24 hours")




if __name__ == "__main__":

    # Extract part of the ETL process
    # all this header are provided in the documentation curl -X GET
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    # trying to see the changes

    # Convert time to Unix timestamp in miliseconds      
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp),
        headers=headers)

    data = r.json()

    # print(data)

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    artist_type = []

    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        artist_type.append(song["track"]["album"]["artists"][0]["type"])

    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps,
        "artist_type" : artist_type
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp", "artist_type"])

    # # validate
    # if check_if_valid_data(song_df):
    #     print('Data Valid, proceed to load stage')

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        artist_type VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
        )
    """
    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exisits in the database")

    conn.close()
    print("Close database successfully")

    print(song_df)