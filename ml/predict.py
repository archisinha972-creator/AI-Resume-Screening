import pandas as pd
import numpy as np
import joblib

# Load save model
model = joblib.load("ml/resume_model.pkl")

# Get information
print("Enter candidate details:")

python_skill = int(input("Python(1/0):"))
pandas_skill = int(input("Pandas(1/0):"))
numpy_skill = int(input("NumPy(1/0):"))
ml_skill = int(input("Machine Learning(1/0):"))
experience = float(input("Experience (yeats):"))
projects = int(input("Number of projects:"))

# create candidate feature
candidate = np.array([[python_skill,pandas_skill,numpy_skill,ml_skill,experience,projects]])

# Predict
prediction = model.predict(candidate)[0]

# Probability
probability = model.predict_proba(candidate)[0][1]

print("\n---Result---")
if prediction == 1:
    print("Prediction : Suitable")
else:
    print("Prediction : Not Suitable")

print(f"Suitability Probability = {probability*100:.2f}%")