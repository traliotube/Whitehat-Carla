import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

dataset = pd.read_csv("./project-234.csv")

football_club = dataset["Club"].value_counts().head(20)
print(football_club)

clubFig = go.Figure(
    data=[go.Pie(labels=football_club.index, values=football_club.values, hole=0.5)]
)
clubFig.show()
