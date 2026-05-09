from flask import Blueprint, request
from config import get_connection

character_bp = Blueprint("characters", __name__)

# =========================================
# OBTENER TODOS LOS PERSONAJES (CON SEARCH)
# =========================================
@character_bp.route("/characters", methods=["GET"])
def get_characters():

    search = request.args.get("search", "").strip()

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            c.id,
            c.name,
            c.birth_date,
            c.main_power,
            c.origin,
            a.name,
            c.anime_id
        FROM characters c
        JOIN anime a ON c.anime_id = a.id
    """

    params = []

    # 🔥 FILTRO TIPO ILIKE
    if search:
        query += " WHERE LOWER(c.name) LIKE LOWER(%s)"
        params.append(f"%{search}%")

    query += " ORDER BY c.id"

    cur.execute(query, params)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    characters = []

    for row in rows:
        characters.append({
            "id": row[0],
            "name": row[1],
            "birth_date": str(row[2]),
            "main_power": row[3],
            "origin": row[4],
            "anime": row[5],
            "anime_id": row[6]
        })

    return characters


# =========================================
# OBTENER PERSONAJE POR ID
# =========================================
@character_bp.route("/characters/<int:id>", methods=["GET"])
def get_character(id):

    conn = get_connection()
    cur = conn.cursor()

    # PERSONAJE
    cur.execute("""
        SELECT
            c.id,
            c.name,
            c.birth_date,
            c.main_power,
            c.origin,
            a.name,
            c.anime_id
        FROM characters c
        JOIN anime a ON c.anime_id = a.id
        WHERE c.id = %s
    """, (id,))

    character = cur.fetchone()

    if not character:
        return {"error": "Personaje no encontrado"}, 404

    # TECNICAS
    cur.execute("""
        SELECT t.name
        FROM technique t
        JOIN character_technique ct
        ON t.id = ct.technique_id
        WHERE ct.character_id = %s
    """, (id,))

    techniques = [row[0] for row in cur.fetchall()]

    # IMAGENES
    cur.execute("""
        SELECT url
        FROM image
        WHERE character_id = %s
    """, (id,))

    images = [row[0] for row in cur.fetchall()]

    # EXTRA DATA
    cur.execute("""
        SELECT description
        FROM extra_data
        WHERE character_id = %s
    """, (id,))

    extra_data = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return {
        "id": character[0],
        "name": character[1],
        "birth_date": str(character[2]),
        "main_power": character[3],
        "origin": character[4],
        "anime": character[5],
        "anime_id": character[6],
        "techniques": techniques,
        "images": images,
        "extra_data": extra_data
    }