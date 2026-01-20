from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import platform

# 1. 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

documents = [
    "부산 여행 바다 맛집",
    "부산 해변 바다 산책",
    "서울 맛집 데이트",
    "제주도 여행 자연"
]
# TF-IDF(Term Frequency-Inverse Document Frequency) : 
# 텍스트 마이닝과 정보 검색에서 특정 단어가 문서 내에서 얼마나 중요한지를 나타내는 통계적 수치입니다.
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(documents)

# print(tfidf)
print(vectorizer.vocabulary_)
print(tfidf.toarray()[0])
print(tfidf.toarray()[1])
print(tfidf.toarray()[2])
print(tfidf.toarray()[3])

#heattmap 챠트 : 밀도를 나타냄

df_tfidf = pd.DataFrame(
    tfidf.toarray(),
    columns=vectorizer.get_feature_names_out(),
    index=[ f"문서 {i}" for i in range(len(documents))]
)

plt.figure(figsize=(12,4))
sns.heatmap(
    df_tfidf,
    # cmap="YlGnBu",
    cmap="Reds",
    annot=True
)
plt.title("문서별 단어 TF-IDF 시각화")
plt.show()

