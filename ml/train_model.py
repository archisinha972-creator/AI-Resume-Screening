import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("data/candidate.csv")

# Feature
x = df[["python","pandas","numpy","machine_learning","experience","projects"]]

#Target
y = df["suitable"]

# Convert data to  NumPy arrays
x = np.array(x)
y = np.array(y)

# split data
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=42,stratify=y)

# Create model
model = LogisticRegression()

# Train model
model.fit(x_train,y_train)

y_pred = model.predict(x_test)

accuracy = accuracy_score(y_test,y_pred)

print("Model trained succesfully.")
print("Accuracy:",accuracy)