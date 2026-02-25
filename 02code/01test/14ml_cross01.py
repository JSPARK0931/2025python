import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate # 교차검증(돌리기만 하는것) 함수
from sklearn.model_selection import StratifiedKFold # 교처검증(순처적으로) class


wine = pd.read_csv("data/wine.csv")
# print(wine.info())
# print(wine.describe())

# feature, target 분리
# numpy가 sklearn에 잘 나옴
data = wine[['alcohol','sugar','pH']].to_numpy()
target = wine['class'].to_numpy()

# test_size 없으면 0.25 (Train: Test = 8:2)
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)

print(X_train.shape, X_test.shape)

# 검증세트(validataion set) 를 만듬
# X_train, y_train  train set를 이용 ( Train_test 8을 8:2로 다시 나눔)
X_subtrain, X_val, y_subtrain, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
print(X_subtrain.shape, X_val.shape)

dt = DecisionTreeClassifier(random_state=42) # class 적용
dt.fit(X_subtrain, y_subtrain)

print(dt.score(X_subtrain, y_subtrain))
print(dt.score(X_val, y_val))

print("--------------------------------------------------")

# 교차검증 ( cross Validation )
# cv : 교차검증 갯수 : 기본값은 5개 cv=5
# fit_time : 모델훈련시간 / score_time : 모델예측시간 /test_score : 모델성능
#scores = cross_validate(dt, X_train,y_train,cv=10)
scores = cross_validate(dt, X_train,y_train) 
print(scores)

# 스코어의 평균점수 
print(f"교차검증 1 점수  : {np.mean(scores['test_score'])}")


scores = cross_validate(dt, X_train,y_train,cv=StratifiedKFold())
# 스코어의 평균점수 
print(f"교차검증 2 점수  : {np.mean(scores['test_score'])}")


spliter = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
scores = cross_validate(dt, X_train,y_train,cv=spliter)
# 스코어의 평균점수 
print(f"교차검증 3 점수  : {np.mean(scores['test_score'])}")

dt.fit(X_train, y_train)
print(dt.score(X_test, y_test))