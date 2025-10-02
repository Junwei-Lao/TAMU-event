import json
import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer


with open("example.json", "r", encoding="utf-8") as f:
    events = json.load(f)

print("Loading model...")
model = SentenceTransformer("sentence-transformers/msmarco-MiniLM-L-6-v3")
model.save("my_local_model")

conn = psycopg2.connect(
    host="localhost",
    database="testerDB",
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

    combined_vector = np.sum(vectors, axis=0)  
    norm = np.linalg.norm(combined_vector)
    
    if norm > 0:
        combined_vector = combined_vector / norm

    combined_vector = combined_vector.tolist()

    cur.execute("""
        INSERT INTO events 
            (event_title, event_date, event_url, event_summary, event_description, event_category, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        e.get("event_title"),
        e.get("event_date"),
        e.get("event_url"),
        e.get("event_summary"),
        e.get("event_description"),
        e.get("event_category"),
        combined_vector
    ))


conn.commit()
cur.close()
conn.close()
print("tester passes")
