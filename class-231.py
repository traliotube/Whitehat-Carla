from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense


dataset = loadtxt("class-230-dataset.csv", delimiter=",")

x = dataset[:, 0:8]
y = dataset[:, 8]

print("value of X are:", x)
print("value of Y are:", y)

model = Sequential()
model.add(Dense(12, input_dim=8, activation="relu"))
model.add(Dense(8, activation="relu"))
model.add(Dense(1, activation="sigmoid"))
model.summary()
