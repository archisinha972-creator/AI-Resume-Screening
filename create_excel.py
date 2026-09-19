import pandas as pd

data = {
    "Name": ["Aarav", "Diya", "Riya", "Kabir"],
    "Python": [1, 1, 1, 1],
    "Pandas": [1, 1, 1, 0],
    "NumPy": [1, 1, 1, 1],
    "Machine_Learning": [1, 0, 1, 0],
    "Experience": [2, 1, 3, 1],
    "Projects": [3, 2, 4, 1]
}

df = pd.DataFrame(data)

df.to_excel(
    "uipath/candidate_input.xlsx",
    sheet_name="Sheet1",
    index=False
)

print("Excel file created successfully!")