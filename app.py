from flask import Flask
from configdb.config import configure_db
from routes import songs_bp

app = Flask(__name__)
configure_db(app)  
app.register_blueprint(songs_bp)  

if __name__ == "__main__":
    app.run(debug=True)