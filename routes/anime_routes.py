from flask import Blueprint
from config import get_connection

anime_bp = Blueprint("anime", __name__)

@anime_bp.route("/anime", methods=["GET"])
def get_animes():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name
        FROM anime
        ORDER BY id
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    animes = []

    for row in rows:
        animes.append({
            "id": row[0],
            "name": row[1]
        })

    return animes