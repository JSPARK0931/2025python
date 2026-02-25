######################################################
### 군집화
######################################################
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# numpy file 을 읽어옮
fruits = np.load("data/fruits_300.npy")

# 3차원을 2차원으로
# fruits_2d = fruits.reshape(300, 100*100)
fruits_2d = fruits.reshape(-1, 100*100)
# print(fruits.shape)
# print(fruits_2d.shape)

# 군집화 종류
km = KMeans(n_clusters=3, random_state=42)
km.fit(fruits_2d)

print(km.labels_)
# 결과값 :
# [2 2 2 2 2 0 2 2 2 2 2 2 2 2 2 2 2 2 0 2 2 2 2 2 2 2 0 2 2 2 2 2 2 2 2 2 2
#  2 2 2 2 2 0 2 0 2 2 2 2 2 2 2 0 2 2 2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 2 2 0 2
#  2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
#  1 1 1 1]
print(np.unique(km.labels_,return_counts=True))
### 결과값 : (array([0, 1, 2], dtype=int32), array([112,  98,  90]))

# 함수 : ratio =1 : 1인치
# **수치 데이터 배열(arr)**을 그리드 형태로 시각화 함수
# . 10개씩 끊어서 여러 줄에 걸쳐 이미지를 출력하도록 설계
def draw_fruits(arr, ratio=1):
    n = len(arr) 
    rows = int(np.ceil(n/10))

    cols = n if rows < 2 else 10
    fig, axs = plt.subplots(rows, cols,figsize=(cols*ratio, rows*ratio), squeeze=False)
    for i in range(rows):
        for j in range(cols):
            if i*10 + j < n:
                axs[i, j].imshow(arr[i*10 + j], cmap='gray_r')
            axs[i, j].axis('off')
    plt.show()

# 군집화별로 이미지출력 
# draw_fruits(fruits[km.labels_ == 0])
# draw_fruits(fruits[km.labels_ == 1])
# draw_fruits(fruits[km.labels_ == 2])

# 평균값이미지 출력
# draw_fruits(km.cluster_centers_.reshape(-1,100,100), ratio=3)

print(km.transform(fruits_2d[100:101]))

print(km.predict(fruits_2d[100:101]))

# 100 번째 과일 이미지 출력
# draw_fruits(fruits[100:101])

knumber = []
for k in range(2,7):
    km = KMeans(n_clusters=k,n_init='auto', random_state=42)
    km.fit(fruits_2d)
    knumber.append(km.inertia_)

plt.plot(range(2,7), knumber)
plt.xlabel('k')
plt.ylabel('inertia')
plt.show()
