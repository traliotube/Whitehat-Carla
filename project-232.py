from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd


dataset = pd.read_csv("project-232-dataset.csv", error_bad_lines=False)

x = dataset.iloc[:, 1:7].values
y = dataset.iloc[:, 8].values

print("value of X are:", x)
print("value of Y are:", y)

model = Sequential()
model.add(Dense(12, input_dim=6, activation="relu"))
model.add(Dense(8, activation="relu"))
model.add(Dense(1, activation="sigmoid"))

model.compile(loss="binary_crossentropy", metrics=["accuracy"])

model.fit(x, y, epochs=250, batch_size=100)

predictions = model.predict(x)
for i in range(5):
    print(
        f"For {x[i].tolist()}, Predicted Value:, {(predictions[i]).round(0)}, Actual Value: {y[i]}"
    )
