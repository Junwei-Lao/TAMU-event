import json
import psycopg2
from pgvector.psycopg2 import register_vector, Vector
from sentence_transformers import SentenceTransformer
import numpy as np




def dbtester():
    PG_HOST = "localhost"
    PG_PORT = ""
    PG_USER = ""
    PG_PASS = ""
    PG_DB   = "eventsdb"
    EMBED_DIM = 384
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASS, dbname=PG_DB
    )
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



def sentencetester():
    EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
    EMBED_DIM = 384