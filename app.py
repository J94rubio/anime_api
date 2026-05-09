import os
from flask import Flask
from flask_cors import CORS

from routes.anime_routes import anime_bp
from routes.character_routes import character_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(anime_bp)
app.register_blueprint(character_bp)

@app.route("/")
def home():
    return {"message": "Anime API funcionando 🚀"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)