# ingest.py #
import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
CHUNK = 500
OVERLAP = 50


def chunk_text(text, size=CHUNK, overlap=OVERLAP):
    words = text.split()
    out = []
    for i in range(0, len(words), size - overlap):
        out.append(" ".join(words[i : i + size]))
    return out


conn = psycopg2.connect(
    dbname="rag", user="ai", password="ai", host="localhost", port="5433"
)
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
register_vector(conn)
cur.execute("""CREATE TABLE IF NOT EXISTS chunks (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    embedding vector(384)
                    ) """)
with open("corpus.txt", encoding="utf-8") as f:
    for para in f.read().split("\n\n"):
        for text in chunk_text(para):
            emb = model.encode(text).tolist()
            cur.execute(
                "INSERT INTO chunks " "(content, embedding) VALUES (%s, %s)",
                (text, emb),
            )

conn.commit()
cur.close()
conn.close()
print("ingested ok")
