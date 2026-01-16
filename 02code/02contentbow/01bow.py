import pandas as pd
from ast import literal_eval # literal : 반복관련
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from tqdm import tqdm

tqdm.pandas()

print("데이터 로드중...")
movies_metadata = pd.read_csv("data/movies_metadata.csv")
links_small = pd.read_csv("data/links_small.csv")
print("데이터 로드완료...")

print("-"*50)

links_small = links_small[links_small["tmdbId"].notnull()]["tmdbId"].astype('int')
movies_metadata_small = movies_metadata[movies_metadata['id'].isin(links_small.astype('str'))]

movies = movies_metadata_small[['title','popularity','genres', 'release_date']].copy() # 깊은복사 : copy 에러 방지

movies['str_genres'] = movies['genres'].fillna('[]') \
    .progress_apply(literal_eval) \
    .progress_apply(lambda x: sorted([i['name'] for i in x]) if isinstance(x, list) else []) \
    .progress_apply(lambda x:" ".join(x) if len(x)>0 else None)

# 일자 : 데이터타입으로 변경
movies['release_date'] = pd.to_datetime(movies['release_date'])

# release date에서 년도만 뽑아서 year 컬럼 생성
movies['year'] = movies['release_date'].dt.year

print(movies.head())

# 결측치를 날리고 날아간 데이터의 index를 재조정해줘야함 reset index
movies = movies.dropna()
movies = movies.reset_index(drop=True)

# BoW :  contents based filtering
bow_vector = CountVectorizer()
# 
genre_mat = bow_vector.fit_transform(movies['str_genres'])

print("유사도 계산중...")
# 코싸인 유사도 측정 (9064, 9064)
similarity_of_genre = cosine_similarity(genre_mat, genre_mat) # data:genre_mat
print("유사도 계산완료...")
print("-"*50)
# 유사도가 높은 영화의 index로 정렬
sorted_similarity_of_genre = similarity_of_genre.argsort()
# index를 역순배열
sorted_similarity_of_genre = sorted_similarity_of_genre[:,::-1]

def recommend(title_name, top_k=5):
    movies_of_title = movies[movies['title'] == title_name] # where 문
    print(f'{title_name}의 장르 : {movies_of_title['str_genres'].values[0]}')

    movies_index_of_title = movies_of_title.index.values[0]
    similar_indexes = sorted_similarity_of_genre[movies_index_of_title,:(top_k*2)]
    print(similar_indexes)

    # 자기자신은 뺌
    similar_indexes = similar_indexes.reshape(-1)
    similar_indexes = similar_indexes[similar_indexes != movies_index_of_title ]

    print(similar_indexes)

    return movies.iloc[similar_indexes].sort_values(by=['year'],ascending=False)[:top_k]


result_movie = recommend('Toy Story', top_k=5)
print(result_movie['title'].tolist())
result_movie = recommend('Jumanji', top_k=5)
print(result_movie['title'].tolist())
