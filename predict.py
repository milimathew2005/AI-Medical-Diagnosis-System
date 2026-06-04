import pickle
import numpy as np

# Load model
model = pickle.load(open("model.pkl", "rb"))

# List of symptoms (same order as dataset)
symptoms = ["fever", "cough", "headache", "fatigue", "sore_throat", "body_pain"]

print("Enter 1 if you have the symptom, 0 if not:\n")
user_input = []

for symptom in symptoms:
    val = int(input(f"Do you have {symptom}? (1/0): "))
    user_input.append(val)

# Convert input to array
user_input = np.array([user_input])

# Predict
prediction = model.predict(user_input)
print("\nMost probable disease:", prediction[0])
