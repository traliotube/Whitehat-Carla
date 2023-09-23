import pandas as pd
from sklearn.neural_network import MLPClassifier

dataset = pd.read_csv("./class-233-new-radar-data.csv")

x = dataset.iloc[:, [2, 4]].values
y = dataset.iloc[:, [5]].values

model = MLPClassifier(
    hidden_layer_sizes=(20),
    random_state=5,
    activation="relu",
    batch_size=200,
    learning_rate_init=0.03,
)

model.fit(x, y)

prediction = model.predict(x)
print("Predicted Data: ", prediction)
