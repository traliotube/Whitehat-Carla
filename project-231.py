from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense


dataset = loadtxt("project-231-dataset.csv", delimiter=",")

x = dataset[:, 4:11]
y = dataset[:, 3]

print("value of X are:", x)
print("value of Y are:", y)

model = Sequential()
model.add(Dense(128, input_dim=8, activation="relu"))
model.add(Dense(100, activation="relu"))
model.add(Dense(56, activation="relu"))
model.add(Dense(2, activation="sigmoid"))
model.summary()
