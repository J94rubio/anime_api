from flask import Blueprint, request
from config import get_connection

character_bp = Blueprint("characters", __name__)

# =========================================
# OBTENER TODOS LOS PERSONAJES (CON SEARCH)
# =========================================
@character_bp.route("/characters", methods=["GET"])
def get_characters():
    """
    Obtener todos los personajes
    ---
    tags:
      - Characters
    parameters:
      - name: search
        in: query
        type: string
        required: false
        description: Filtra personajes por nombre (insensible a mayúsculas)
        example: seiya
    responses:
      200:
        description: Lista de personajes
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
                example: Seiya de Pegaso
              birth_date:
                type: string
                example: "1975-01-01"
              main_power:
                type: string
                example: Meteoros de Pegaso
              origin:
                type: string
                example: Japón
              anime:
                type: string
                example: Saint Seiya
              anime_id:
                type: integer
                example: 1
    """
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

    if search:
        query += " WHERE LOWER(c.name) LIKE LOWER(%s)"
        params.append(f"%{search}%")

    query += " ORDER BY c.id"

    cur.execute(query, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "birth_date": str(row[2]),
            "main_power": row[3],
            "origin": row[4],
            "anime": row[5],
            "anime_id": row[6],
        }
        for row in rows
    ]


# =========================================
# OBTENER PERSONAJE POR ID
# =========================================
@character_bp.route("/characters/<int:id>", methods=["GET"])
def get_character(id):
    """
    Obtener personaje por ID
    ---
    tags:
      - Characters
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del personaje
        example: 1
    responses:
      200:
        description: Detalle completo del personaje
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            birth_date:
              type: string
            main_power:
              type: string
            origin:
              type: string
            anime:
              type: string
            anime_id:
              type: integer
            techniques:
              type: array
              items:
                type: string
              example: ["Meteoros de Pegaso", "Galaxian Explosion"]
            images:
              type: array
              items:
                type: string
              example: ["https://imagen.com/seiya.jpg"]
            extra_data:
              type: array
              items:
                type: string
      404:
        description: Personaje no encontrado
    """
    conn = get_connection()
    cur = conn.cursor()

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

    cur.execute("""
        SELECT t.name
        FROM technique t
        JOIN character_technique ct ON t.id = ct.technique_id
        WHERE ct.character_id = %s
    """, (id,))
    techniques = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT url FROM image WHERE character_id = %s", (id,))
    images = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT description FROM extra_data WHERE character_id = %s", (id,))
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
        "extra_data": extra_data,
    }