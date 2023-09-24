import pandas as pd
import pickle

# load it again
savedModelFile = open("class-234-model.pkl", "rb")
savedModel = pickle.load(savedModelFile)

# test model

# carData = {"throttle": [0.164332455], "distance": [10.674762726]}
carData = {"throttle": [0.164332455], "steer": [-0.5]}

# data = pd.DataFrame(carData, columns=["throttle", "distance"])
data = pd.DataFrame(carData, columns=["throttle", "steer"])
predictedData = savedModel.predict(data)
print(f"Your Prediction is: {predictedData}")
