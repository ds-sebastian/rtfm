from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1", cache_folder="cache")

query_embedding = model.encode("Hello, how are you?")

print(query_embedding)
