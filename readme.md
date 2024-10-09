# Backend Developer Assignment (Python, MongoDB)

## Overview

This project is an API built using Flask and MongoDB that allows users to interact with a collection of songs. It provides various functionalities such as retrieving songs, filtering by difficulty, searching, and managing ratings.

## Setup

### 1. Install dependencies and import data

Run the following commands to install the required dependencies and set up the database:

```bash
sudo apt install python3 python3-pip
pip3 install Flask
pip3 install Flask-PyMongo
pip3 install Flask-Paginate
```

### 2. Run MongoDB in Docker
```bash
docker run --detach --name songs_db --publish 127.0.0.1:27017:27017 mongo:4.4
```
### 3. Import the data
```bash
mongoimport --db songs_db --collection songs --file songs.json --jsonArray
```
### 4. Run the flask app
```bash
python3 app.py
```
