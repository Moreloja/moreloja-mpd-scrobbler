#!/usr/bin/env python3

"""
Scrobble songs listened to on mpd to moreloja.
"""

import os
import time
from datetime import datetime, timezone

import pymongo
from mpd import MPDClient


def connect_mongodb():
    """Connect to mongodb and return the playback-info collection."""
    mongo_host = os.environ.get("MONGO_HOST")
    mongo_port = os.environ.get("MONGO_PORT")
    mongo_db = os.environ.get("MONGO_DB_NAME")
    mongo_user = os.environ.get("MONGO_USER")
    mongo_password = os.environ.get("MONGO_PASSWORD")

    # Connect to MongoDB
    if mongo_user and mongo_password:
        mongo_client = pymongo.MongoClient(
            f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"
        )
    else:
        mongo_client = pymongo.MongoClient(f"mongodb://{mongo_host}:{mongo_port}")

    db = mongo_client[mongo_db]
    collection = db["playback-info"]

    return collection


def save_currentsong(mpd_client: MPDClient, collection):
    """
    Contains the main loop to query mpd and save played songs.
    """
    # Get current song from mpd
    song_start_time = datetime.now(timezone.utc)
    previous_song = mpd_client.currentsong()
    previous_status = mpd_client.status()

    # Main Loop
    while True:
        current_song = mpd_client.currentsong()
        current_status = mpd_client.status()

        if current_song != previous_song:
            # songs that have no title will not be scrobbled
            if previous_song.get("title", None) is not None:
                playback_info = {
                    "Artist": previous_song.get("artist", None),
                    "artistsort": previous_song.get("artistsort", None),
                    "albumartist": previous_song.get("albumartist", None),
                    "albumartistsort": previous_song.get("albumartistsort", None),
                    "timestamp": song_start_time,
                    "timestamp_end": datetime.now(timezone.utc),
                    "Album": previous_song.get("album", None),
                    "Name": previous_song.get("title", None),
                    "label": previous_song.get("label", None),
                    "Provider_musicbrainzalbum": previous_song.get(
                        "musicbrainz_albumid", None
                    ),
                    "Provider_musicbrainzalbumartist": previous_song.get(
                        "musicbrainz_albumartistid", None
                    ),
                    "Provider_musicbrainzartist": previous_song.get(
                        "musicbrainz_artistid", None
                    ),
                    "Provider_musicbrainzreleasegroup": previous_song.get(
                        "musicbrainz_releasetrackid", None
                    ),
                    "Provider_musicbrainztrack": previous_song.get(
                        "musicbrainz_trackid", None
                    ),
                    "musicbrainz_workid": previous_song.get("musicbrainz_workid", None),
                    "Server": "mpd",
                    "ServerVersion": mpd_client.mpd_version,
                    "date": previous_song.get("date", None),
                    "originaldate": previous_song.get("originaldate", None),
                    "Year": int(previous_song["originaldate"][:4])
                    if previous_song.get("originaldate", "")
                    else None,
                    "disc": previous_song.get("disc", None),
                    "track": previous_song.get("track", None),
                    "genre": previous_song.get("genre", None),
                    "playback_position_seconds": float(
                        previous_status.get("elapsed", "0")
                    ),
                    "run_time": float(previous_status.get("duration", "0")),
                    "playback_info_schema_version": 2,
                }

                collection.insert_one(playback_info)

                print(f"Playback of song {previous_song['title']} saved to database.")

            song_start_time = datetime.now(timezone.utc)
            previous_song = current_song

        # Update previous status every loop. This allows us to get the
        # elapsed time before the song changes
        previous_status = current_status

        # Sleep for 1 seconds
        time.sleep(1)


def main():
    """Main entry point"""
    # Connect to mpd
    mpd_client = MPDClient()
    mpd_host = os.environ.get("MPD_HOST")
    mpd_port = os.environ.get("MPD_PORT")
    mpd_client.connect(mpd_host, mpd_port)

    # Connect to MongoDB
    collection = connect_mongodb()

    # Get and save current song
    save_currentsong(mpd_client, collection)


if __name__ == "__main__":
    main()
