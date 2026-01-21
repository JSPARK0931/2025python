from sentence_transformers import SentenceTransformer, util

# 영어기준 model
model = SentenceTransformer("all-MiniLM-L6-v2")
# 한글기준 model은 별도 있음 
# 한국어 문장 임베딩에 최적화된 로버타(RoBERTa) 모델
model1 = SentenceTransformer("jhgan/ko-sroberta-multitask")

sentences = [
    "I want to travel to Busan",
    "I want to see the sea in Busan",
    "The stock market is difficult"
]

sentences1 = [
    "부산 여행 가고 싶다",
    "부산 바다 보고 싶다",
    "주식 시장이 어렵다"
]


embeddings = model.encode(sentences)
similarity = util.cos_sim(embeddings[0], embeddings[1])
similarity1 = util.cos_sim(embeddings[0], embeddings[2])

print("문장 1 : ", sentences[0])
print("문장 2 : ", sentences[1])
print("유사도 점수 : ", similarity)

print("문장 1 : ", sentences[0])
print("문장 3 : ", sentences[2])
print("유사도 점수 : ", similarity1)

# ---------------------------------------------------
# 결과값 : cosine 유사도이므로 1에 가까울수록 유사도가 높다
# ---------------------------------------------------
# 문장 1 :  I want to travel to Busan
# 문장 2 :  I want to see the sea in Busan
# 유사도 점수 :  tensor([[0.6718]])
# 문장 1 :  I want to travel to Busan
# 문장 3 :  The stock market is difficult
# 유사도 점수 :  tensor([[0.0770]])

embeddings1 = model1.encode(sentences1)
similarity2   = util.cos_sim(embeddings1[0], embeddings1[1])
similarity2_1 = util.cos_sim(embeddings1[0], embeddings1[2])

print("문장 1 : ", sentences1[0])
print("문장 2 : ", sentences1[1])
print("유사도 점수 : ", similarity2)

print("문장 1 : ", sentences1[0])
print("문장 3 : ", sentences1[2])
print("유사도 점수 : ", similarity2_1)


