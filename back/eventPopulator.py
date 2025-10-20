import json
import numpy as np
import psycopg2
from psycopg2 import sql
from sentence_transformers import SentenceTransformer
import re
from nltk.corpus import stopwords
import os


def extract_keywords(text: str, top_k: int = 5):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    stops = set(stopwords.words('english'))
    keywords = [w for w in words if w not in stops]
    freq = {}
    for w in keywords:
        freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.keys(), key=lambda x: freq[x], reverse=True)
    return sorted_words[:top_k]


def searcher(query_text: str, TableName: str, top_k: int = 20, useOldModel: bool = True):
    model_path = os.path.join(os.path.dirname(__file__), "my_local_model")
    model = SentenceTransformer(model_path if useOldModel else "sentence-transformers/multi-qa-MiniLM-L6-cos-v1")

    # Get normalized query embedding
    query_vec = model.encode(query_text, normalize_embeddings=True)

    # Extract keywords for hybrid scoring
    keywords = extract_keywords(query_text)
    keyword_query = " | ".join(keywords) if keywords else query_text

    print(f"🔍 Hybrid search query: {keyword_query}")

    conn = psycopg2.connect(
        host="localhost",
        database="eventsdb",
        user="postgres",
        password="weidai21"
    )
    cur = conn.cursor()

    # Ensure trigram extension exists (safe to run each time)
    cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    # Hybrid query: vector + text relevance + trigram fuzzy
    query = sql.SQL("""
        SELECT 
            event_title,
            event_dates,
            event_url,
            event_summary,
            event_description,
            (
                0.3 * (1 - (embedding <#> %s::vector)) +  -- semantic similarity
                0.45 * ts_rank_cd(
                    to_tsvector('english',
                        COALESCE(event_title, '') || ' ' ||
                        COALESCE(event_summary, '') || ' ' ||
                        COALESCE(event_description, '')
                    ),
                    websearch_to_tsquery('english', %s)
                ) +
                0.25 * greatest(
                    similarity(COALESCE(event_title, ''), %s),
                    similarity(COALESCE(event_summary, ''), %s),
                    similarity(COALESCE(event_description, ''), %s)
                )
            ) AS score
        FROM {table}
        ORDER BY score DESC
        LIMIT %s;
    """).format(table=sql.Identifier(TableName))

    cur.execute(query, (
        query_vec.tolist(),      # semantic vector
        keyword_query,           # tsquery
        query_text,              # trigram fuzzy (title)
        query_text,              # trigram fuzzy (summary)
        query_text,              # trigram fuzzy (desc)
        top_k
    ))

    rows = cur.fetchall()
    results = []
    for row in rows:
        results.append({
            "event_title": row[0],
            "event_date": row[1],
            "event_url": row[2],
            "event_summary": row[3],
            "event_description": row[4],
            "similarity": float(row[5])
        })

    cur.close()
    conn.close()
    return results


def populator(TableName: str, useOldModel: bool = False):
    file_path = os.path.join(os.path.dirname(__file__), f"{TableName}.json")
    with open(file_path, "r", encoding="utf-8") as f:
        events = json.load(f)

    print("Loading model...")
    model_path = os.path.join(os.path.dirname(__file__), "my_local_model")
    model = SentenceTransformer(model_path if useOldModel else "sentence-transformers/multi-qa-MiniLM-L6-cos-v1")

    if not useOldModel:
        model.save("my_local_model")

    conn = psycopg2.connect(
        host="localhost",
        database="eventsdb",
        user="postgres",
        password="weidai21"
    )
    cur = conn.cursor()

    cur.execute(sql.SQL("TRUNCATE TABLE {table} RESTART IDENTITY;").format(table=sql.Identifier(TableName)))
    conn.commit()
    print(f"Table {TableName} cleared.")

    for e in events:
        text_to_embed = " ".join([
            e.get("event_title", ""),
            e.get("event_summary", ""),
            e.get("event_description", ""),
            e.get("event_category", "")
        ]).strip()

        if not text_to_embed:
            continue

        emb = model.encode(text_to_embed, normalize_embeddings=True)
        emb_list = emb.tolist()

        cur.execute(
            sql.SQL("""
                INSERT INTO {table}
                    (event_title, event_dates, event_url, event_summary, event_description, event_category, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """).format(table=sql.Identifier(TableName)),
            (
                e.get("event_title"),
                e.get("event_dates"),
                e.get("event_url"),
                e.get("event_summary"),
                e.get("event_description"),
                e.get("event_category"),
                emb_list
            )
        )

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {len(events)} events with embeddings into table {TableName}")
