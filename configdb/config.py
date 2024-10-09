from flask_pymongo import PyMongo

mongo = PyMongo()

def configure_db(app):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/songs_db"
    mongo.init_app(app)
