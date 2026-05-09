from flask import Blueprint
from config import get_connection

anime_bp = Blueprint("anime", __name__)

@anime_bp.route("/anime", methods=["GET"])
def get_animes():
    """
    Obtener lista de animes
    ---
    tags:
      - Anime
    responses:
      200:
        description: Lista de animes
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: Saint Seiya
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM anime ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": row[0], "name": row[1]} for row in rows]