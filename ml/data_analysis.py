import pandas as pd
df = pd.read_csv("data/candidate.csv")
print("Candidate Data:")
print(df)

print("\nNumber of candiates:")
print(len(df))

print("\nAverage experience:")
print(df["experience"].mean())

print("\nAverage number of projects:")
print(df["projects"].mean())

print("Candidate with Machine Learning:")
print(df[df["machine_learning"]==1])
