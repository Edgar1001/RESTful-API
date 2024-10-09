from configdb.config import mongo

def get_songs_collection():
    return mongo.db.songs

def get_song_by_id(song_id):
    return get_songs_collection().find_one({"_id": song_id})