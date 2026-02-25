print("test")

import tensorflow as tf
import numpy as np

x = np.array([1,2,3,4],dtype=float)
y = np.array([2,4,6,8],dtype=float)

model = tf.keras.sequential([
    tf.keras.layers.Dense(1,input_shape(1,))
])

model.compile(
    optimizer ='sgd',
    loss='mse'
)
#verboss : 1 : 보임 , 0 : 안보임, 2 :축약
model.fit(x,y,epochs=200,verboss=2)

print(model.predict(np.array([6])))

model = tf.keras.Sqeuntial()
model.add(ft.keras.layers.Dense(1,input_shape(1,)))

model.compile(
    optimizer="adam",
    loss="mse"
)

model.fit(x,y,epochs=200)
print(model.predict(np.array([6])))