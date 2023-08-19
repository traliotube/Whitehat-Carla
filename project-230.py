import pandas as pd

dataset = pd.read_csv("project-230-dataset.csv")
print(dataset.shape)
print(len(dataset.columns))
print(dataset.columns)
print("Display empty row data:", dataset.loc[:, dataset.isna().any()])
