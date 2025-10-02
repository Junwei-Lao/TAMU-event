import json
import numpy as np
import psycopg2
from psycopg2 import sql
from sentence_transformers import SentenceTransformer

def main(TableName: str, useOldModel: bool = False):
    with open("events.json", "r", encoding="utf-8") as f:
        events = json.load(f)

    print("Loading model...")
    if useOldModel:
        model = SentenceTransformer("my_local_model")
    else:
        model = SentenceTransformer("sentence-transformers/msmarco-MiniLM-L-6-v3")
        model.save("my_local_model")

    conn = psycopg2.connect(
        host="localhost",
        database="eventsdb",
        user="postgres",
        password=""
    )
    cur = conn.cursor()

    for e in events:
        vectors = []
        for field in ["event_title", "event_summary", "event_description", "event_category"]:
            text = e.get(field, "")
            if text and text.strip():
                vec = model.encode(text)
                vectors.append(vec)

        if not vectors:
            continue

        combined_vector = np.sum(vectors, axis=0)
        norm = np.linalg.norm(combined_vector)
        if norm > 0:
            combined_vector = combined_vector / norm

        combined_vector = combined_vector.tolist()

        cur.execute(
            sql.SQL("""
                INSERT INTO {table} 
                    (event_title, event_date, event_url, event_summary, event_description, event_category, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """).format(table=sql.Identifier(TableName)),
            (
                e.get("event_title"),
                e.get("event_date"),
                e.get("event_url"),
                e.get("event_summary"),
                e.get("event_description"),
                e.get("event_category"),
                combined_vector
            )
        )

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {len(events)} events with embeddings into table {TableName}")



if __name__ == "__main__":
    main("eventsA", True)
