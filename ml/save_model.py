import pandas as pd 
import numpy as np
import joblib

from sklearn.linear_model import LogisticRegression

# load dataset
df = pd.read_csv("data/candidate.csv")

# features
x = np.array(df[["python","pandas","numpy","machine_learning","experience","projects"]])
y = np.array(df["suitable"])

# Train mode
model = LogisticRegression()
model.fit(x,y)

# Save model
joblib.dump(model,"ml/resume_model.pkl")

print("Model trained and saved successfully.")