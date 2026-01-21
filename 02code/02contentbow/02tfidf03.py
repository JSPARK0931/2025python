import pandas as pd
from ast import literal_eval
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances

# 유사영화 TOP 5 구하기
def recomm_of_euclidean(title_name, top_k=30):
    # movie에서 title과 입력제목을 찾음
    movie_of_title = movies[movies['title'] == title_name]
    print(f"{title_name} 의 장르 : {movie_of_title['str_genres_keywords'].values[0]}")
    # print(f"{title_name}")
    # print(f"{movie_of_title['str_genres_keywords'].values[0]}")
    
    movie_index_of_title = movie_of_title.index.values[0]
    print(f"\n index : {movie_index_of_title}")

    similar_indexes = sorted_similarity_of_euclidean[movie_index_of_title,:top_k * 2]
    print(similar_indexes)
    print(similar_indexes.shape)
    similar_indexes = similar_indexes.reshape(-1) # 
    similar_indexes = similar_indexes[similar_indexes != movie_index_of_title]
    print(similar_indexes)

    return movies.iloc[similar_indexes].sort_values(by=['popularity_log','year'], ascending=False)[:10]

movies_metadata = pd.read_csv("data/movies_metadata.csv")
links_small = pd.read_csv("data/links_small.csv")
movies_keywords = pd.read_csv("data/keywords.csv")

print(links_small.head())

links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')
movies_metadata = movies_metadata[movies_metadata['id'].isin(links_small.astype('str'))]

movies = movies_metadata[['id', 'title', 'genres', 'popularity', 'release_date']]

movies_keywords['id'] = movies_keywords['id'].astype('str')
movies = movies.merge(movies_keywords,on='id')

print(movies.head())

movies['genres'] = movies['genres'].fillna('[]') \
                    .apply(literal_eval) \
                    .apply(lambda x: sorted( i['name'] for i in x) if isinstance(x,list) else [])


movies['keywords'] = movies['keywords'].fillna('[]') \
                    .apply(literal_eval) \
                    .apply(lambda x: sorted( i['name'] for i in x) if isinstance(x,list) else [])


# 장르와 키워드를 붙임
movies['str_genres_keywords'] = movies['genres'] + movies['keywords']

print(movies[['genres', 'keywords', 'str_genres_keywords']])

# sort
movies['str_genres_keywords'] = movies['str_genres_keywords'] \
                                .apply(lambda x:sorted(list(x))) \
                                .apply(lambda x: " ".join(x) if len(x) > 0 else None)

# 개봉일 전처리
movies['release_date'] = pd.to_datetime(movies['release_date'])
movies['year'] = movies['release_date'].dt.year

print(movies)
# 숫자형태로 변환
movies['popularity'] = movies['popularity'].astype(float)

sns.histplot(movies['popularity'])
# plt.show()
movies['popularity_log'] = np.log(movies['popularity'])
sns.histplot(movies['popularity_log'])

# 결측치 test
print(movies.isnull().sum())

movies  = movies.dropna().reset_index(drop=True)
print(movies.isnull().sum())

### Euclidean Distances(유클리드 거리)
tfidf_vectorizer = TfidfVectorizer()
tfidf_mat = tfidf_vectorizer.fit_transform(movies['str_genres_keywords'])
arr_tfidf = tfidf_mat.toarray()

similarity_of_euclidean = euclidean_distances(arr_tfidf, arr_tfidf)
print(similarity_of_euclidean)
sorted_similarity_of_euclidean = similarity_of_euclidean.argsort()

print(similarity_of_euclidean[0])
print(sorted_similarity_of_euclidean[0])

print(movies[['title','str_genres_keywords']].iloc[[0,1477]])

recomm_movies = recomm_of_euclidean("Robin Hood")
print(recomm_movies[['title','popularity_log','year']])