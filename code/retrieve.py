# retrieve.py #
import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
conn = psycopg2.connect(
    dbname="rag", user="ai", password="ai", host="localhost", port="5433"
)
register_vector(conn)
cur = conn.cursor()

question = "What does our support team cover?"
emb = model.encode(question).tolist()
cur.execute(
    "SELECT content, 1 - (embedding <=> %s::vector) AS score FROM chunks ORDER BY embedding <=> %s::vector LIMIT 3",
    (emb, emb),
)
for content, score in cur.fetchall():
    print(round(score, 3), content[:120])
cur.close()
conn.close()
