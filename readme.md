# Backend Developer Assignment (Python, MongoDB)

## Setup

1. **Install dependencies**
   sudo apt install python3 python3-pip
   pip3 install Flask
   pip3 install Flask-pymongo
   pip3 install Flask-Paginate

2. **Run MongoDB in Docker**

docker run --detach --name songs_db --publish 127.0.0.1:27017:27017 mongo:4.4

3. **Import the data**
mongoimport --db songs_db --collection songs --file songs.json --jsonArray

3. **Run the flask app**
python3 app.py
