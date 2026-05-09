import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from routes.anime_routes import anime_bp
from routes.character_routes import character_bp

app = Flask(__name__)
CORS(app)

# Configuración de Swagger
app.config["SWAGGER"] = {
    "title": "Anime API",
    "description": "API para consultar personajes y animes",
    "version": "1.0.0",
    "uiversion": 3,
}
Swagger(app)

app.register_blueprint(anime_bp)
app.register_blueprint(character_bp)

@app.route("/")
def home():
    return {"message": "Anime API funcionando 🚀"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)