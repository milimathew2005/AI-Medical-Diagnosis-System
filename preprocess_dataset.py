import pandas as pd

# Load your dataset.csv
data = pd.read_csv("dataset.csv")

# Columns containing symptoms
symptom_cols = [f"Symptom_{i}" for i in range(1, 10)]

# Step 1: Collect all unique symptoms
all_symptoms = set()
for col in symptom_cols:
    all_symptoms.update(data[col].dropna().unique())

all_symptoms = sorted(all_symptoms)  # sort for consistency

# Step 2: Create new DataFrame with 0/1 for each symptom
processed_data = pd.DataFrame(columns=list(all_symptoms) + ["disease"])

for idx, row in data.iterrows():
    row_dict = {symptom: 0 for symptom in all_symptoms}
    for col in symptom_cols:
        if pd.notna(row[col]):
            row_dict[row[col]] = 1
    row_dict["disease"] = row["Disease"]
    # Use pd.concat instead of append
    processed_data = pd.concat([processed_data, pd.DataFrame([row_dict])], ignore_index=True)

# Step 3: Save the processed dataset
processed_data.to_csv("processed_dataset.csv", index=False)
print("Processed dataset saved as processed_dataset.csv")

import pandas as pd
import pickle

# Load processed dataset
data = pd.read_csv("processed_dataset.csv")

# Extract symptom columns
symptoms = list(data.columns)
symptoms.remove("disease")  # remove target column

# Save to pickle file
pickle.dump(symptoms, open("symptoms.pkl", "wb"))

print("symptoms.pkl created successfully!")
