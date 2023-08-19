from numpy import loadtxt

dataset = loadtxt("class-230-dataset.csv", delimiter=",")

x = dataset[:, 0:8]
y = dataset[:, 8]

print("value of X are:", x)
print("value of Y are:", y)
