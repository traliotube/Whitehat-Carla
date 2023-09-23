import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

dataset = pd.read_csv("./project-234.csv")

goal_column = dataset["Goals"]
sorted_goal_values = (goal_column.groupby(dataset["Club"]).sum()).sort_values(
    ascending=False
)
print(sorted_goal_values)

epl_top_goals = dataset.sort_values(by=["Goals"], ascending=False)[:10]
print(epl_top_goals)

fig = px.bar(
    epl_top_goals,
    x="Name",
    y="Goals",
    color="Goals",
    hover_data=["Club", "Age"],
    text="Goals",
)
fig.show()
