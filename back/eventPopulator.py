import json
import psycopg2
from pgvector.psycopg2 import register_vector, Vector
from sentence_transformers import SentenceTransformer
import numpy as np

# -------------------- CONFIG --------------------
PG_HOST = "localhost"
PG_PORT = "5432"
PG_USER = "postgres"
PG_PASS = "yourpassword"
PG_DB   = "eventsdb"

EVENTS_FILE = "events.json"

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
EMBED_DIM = 384
# ------------------------------------------------


def dbInitializer():
    try:
        conn = connect()
        create_table_and_extension(conn)
    except:
        print("Failed to initialize database")




def connect():
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASS, dbname=PG_DB
    )
    return conn


def create_table_and_extension(conn):
    cur = conn.cursor()
    register_vector(conn)
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()

    sql = f"""
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        event_title TEXT NOT NULL,
        event_date TEXT NOT NULL,
        event_url TEXT,
        event_summary TEXT,
        event_description TEXT,
        event_category TEXT,
        embedding vector({EMBED_DIM}) NOT NULL
    );
    """
    cur.execute(sql)
    conn.commit()
    cur.close()
    print("Table ready.")


def embed_texts(model, texts):
    emb = model.encode(texts, convert_to_numpy=True)
    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return emb / norms


def insert_events(conn, model, events):
    cur = conn.cursor()
    sql = """
    INSERT INTO events (event_title, event_date, event_url, event_summary, event_description, event_category, embedding)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """

    texts = []
    for e in events:
        desc = e.get("event_summary", "")
        details = e.get("event_description", "")
        category = e.get("event_category", "")
        combined = f"{desc}. {details}. Category: {category}"
        texts.append(combined)

    embeddings = embed_texts(model, texts)

    ids = []
    for e, vec in zip(events, embeddings):
        v = Vector(vec.tolist())
        cur.execute(sql, (
            e.get("event_title"),
            e.get("event_date"),
            e.get("event_url"),
            e.get("event_summary"),
            e.get("event_description"),
            e.get("event_category"),
            v
        ))
        ids.append(cur.fetchone()[0])

    conn.commit()
    cur.close()
    print(f"Inserted {len(ids)} events.")


def test_search(conn, model, query, top_k=15):
    cur = conn.cursor()
    q_emb = embed_texts(model, [query])[0]
    q_vec = Vector(q_emb.tolist())

    sql = """
    SELECT id, event_title, event_date, event_url, event_category,
           embedding <-> %s AS distance
    FROM events
    ORDER BY distance
    LIMIT %s;
    """
    cur.execute(sql, (q_vec, top_k))
    rows = cur.fetchall()
    print(f"\nTop {top_k} matches for: '{query}'")
    for r in rows:
        print(f"- id={r[0]} | {r[1]} | {r[2]} | {r[3]} | category={r[4]} | dist={r[5]:.4f}")
    cur.close()


def main():
    print("Starting...")
    conn = connect()
    create_table_and_extension(conn)

    print("Loading events from JSON:", EVENTS_FILE)
    with open(EVENTS_FILE, "r") as f:
        events = json.load(f)

    model = SentenceTransformer(EMBED_MODEL_NAME)
    insert_events(conn, model, events)

    test_search(conn, model, "math events")
    test_search(conn, model, "football match")

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
