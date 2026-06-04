import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Load processed dataset
data = pd.read_csv("processed_dataset.csv")  # Your binary symptom dataset

X = data.drop("disease", axis=1)
y = data["disease"]

# Optional: Load symptom weights
weights_df = pd.read_csv("symptom-severity.csv")  # columns: Symptom, Weight
weights = dict(zip(weights_df['Symptom'], weights_df['Weight']))

# Apply weights to X
for col in X.columns:
    if col in weights:
        X[col] = X[col] * weights[col]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Classifier
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", round(accuracy_score(y_test, y_pred)*100,2), "%")
print(classification_report(y_test, y_pred))

# Save model & symptoms
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("symptoms.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("Model and symptoms saved successfully!")
