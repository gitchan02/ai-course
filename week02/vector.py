import ollama
import numpy as np

def emb(text):
    r = ollama.embed(model="bge-m3", input=text)
    return np.array(r.embeddings[0])
def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

v = emb("사과")
print("벡터 길이:", len(v))
print("앞 5개 값:", v[:5])

print("사과-배:", round(cos(emb("사과"), emb("배")), 3))
print("사과-자동차:", round(cos(emb("사과"), emb("자동차")), 3))