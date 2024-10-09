from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from flask_paginate import Pagination
from bson.objectid import ObjectId


songs_bp = Blueprint('songs', __name__)


def get_songs_collection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.songs_db
    return db.songs
def serialize(data):
    """Recursively convert ObjectId instances to strings."""
    if isinstance(data, dict):
        return {key: serialize(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

# A: Return a paginated list of songs
@songs_bp.route('/songs', methods=['GET'])
def get_songs():
    songs_collection = get_songs_collection()
    
    page = request.args.get('page', 1, type=int)  
    per_page = request.args.get('per_page', 10, type=int) 
    total = songs_collection.count_documents({})  
    songs = list(songs_collection.find().skip((page - 1) * per_page).limit(per_page))
    pagination = Pagination(page=page, total=total, per_page=per_page, record_name='songs', css_framework='bootstrap4')
    return jsonify({
        'total': total,
        'songs': serialize(songs),  
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': pagination.total_pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
        }
    }), 200

# B: Return the average difficulty for all songs or filtered by level
@songs_bp.route('/average_difficulty', methods=['GET'])
def average_difficulty():
    songs_collection = get_songs_collection()
    level = request.args.get('level', None, type=int)
    if level:
        pipeline = [
            {'$match': {'level': level}},
            {'$group': {'_id': None, 'average_difficulty': {'$avg': '$difficulty'}}}
        ]
    else:
        pipeline = [
            {'$group': {'_id': None, 'average_difficulty': {'$avg': '$difficulty'}}}
        ]
    result = list(songs_collection.aggregate(pipeline))
    average = result[0]['average_difficulty'] if result else 0
    return jsonify({'average_difficulty': average}), 200

# C: Return songs matching the search string
@songs_bp.route('/search', methods=['GET'])
def search_songs():
    songs_collection = get_songs_collection()
    message = request.args.get('message', '', type=str)
    regex = {'$regex': message, '$options': 'i'}  
    
    songs = list(songs_collection.find({'$or': [{'title': regex}, {'artist': regex}]}))
    return jsonify({'songs': serialize(songs)}), 200  


# D: Add ratings
@songs_bp.route('/rate', methods=['POST'])
def add_rating():
    songs_collection = get_songs_collection()
    song_id = request.json.get('song_id')
    rating = request.json.get('rating')  

    try:
        rating = int(rating)  
    except (ValueError, TypeError):  
        return jsonify({'error': 'Invalid rating value.'}), 400

    if rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5.'}), 400
    songs_collection.update_one(
        {'_id': ObjectId(song_id)},
        {'$push': {'ratings': rating}}
    )
    return jsonify({'message': 'Rating added successfully.'}), 201


# E: Return average, lowest and highest rating of a given song
@songs_bp.route('/ratings/<song_id>', methods=['GET'])
def get_ratings(song_id):
    songs_collection = get_songs_collection()
    song = songs_collection.find_one({'_id': ObjectId(song_id)})

    if not song or 'ratings' not in song:
        return jsonify({'error': 'Song not found or has no ratings.'}), 404

    ratings = song['ratings']
    average_rating = sum(ratings) / len(ratings) if ratings else 0
    return jsonify({
        'average_rating': average_rating,
        'lowest_rating': min(ratings),
        'highest_rating': max(ratings)
    }), 200
