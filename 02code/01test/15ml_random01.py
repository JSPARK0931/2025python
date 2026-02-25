### Tree enemble (앙상블)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate # 교차검증(돌리기만 하는것) 함수
from sklearn.model_selection import StratifiedKFold # 교처검증(순처적으로) class
from sklearn.ensemble import RandomForestClassifier


wine = pd.read_csv("data/wine.csv")

# feature, target 분리
data = wine[['alcohol','sugar','pH']].to_numpy()
target = wine['class'].to_numpy()

# test_size 없으면 0.25 (Train: Test = 8:2)
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)

# RandomForestClassifier class
# njobs : cpu core할당 n_jobs=-1 : cpu 전체할당 , nn_estimators=100 : 결정트리갯수 기본값은 100
rf = RandomForestClassifier(n_jobs=-1, random_state=42)

scores = cross_validate(rf, X_train, y_train, return_train_score= True, n_jobs=-1)
print(scores)

print(np.mean(scores['train_score']))
print(np.mean(scores['test_score']))

rf.fit(X_train, y_train)
print(rf.predict(X_test[:5]))
print(rf.feature_importances_)
