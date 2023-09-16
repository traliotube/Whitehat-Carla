import pandas as pd

df = pd.read_csv("./project-233.csv")

df["Total_marks_obtained"] = df.iloc[:, [2, 3, 4]].sum(axis=1)

df.loc[df["Total_marks_obtained"] > 250, "Grade"] = "A"
df.loc[df["Total_marks_obtained"] < 250, "Grade"] = "B"

df["Percentage"] = (df["Total_marks_obtained"] / df["Overall_Total"]) * 100


df.to_csv("project-233-new-marks.csv", index=False)
print(df)
