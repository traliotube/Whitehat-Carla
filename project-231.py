from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd


dataset = pd.read_csv("project-231-dataset.csv", error_bad_lines=False)

x = dataset.iloc[:, 4:11].values
y = dataset.iloc[:, 3].values

print("value of X are:", x)
print("value of Y are:", y)

model = Sequential()
model.add(Dense(128, input_dim=8, activation="relu"))
model.add(Dense(100, activation="relu"))
model.add(Dense(56, activation="relu"))
model.add(Dense(2, activation="sigmoid"))
model.summary()
