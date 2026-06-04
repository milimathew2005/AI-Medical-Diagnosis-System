# AI Medical Diagnosis System

An interactive, AI-powered medical diagnosis web application and machine learning pipeline. This system predicts potential diseases based on user-inputted symptoms. It includes a user-friendly Flask-based web interface, an interactive NLP chatbot, data preprocessing tools, and machine learning model training scripts.

> [!WARNING]
> **Medical Disclaimer:** This application is for educational/demo purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a healthcare professional for medical concerns.

---

## 🚀 Features

- **Flask Web Dashboard:** A visual interface where users can select symptoms and receive probabilistic disease predictions.
- **AI Chatbot (NLP-driven):** An interactive chatbot built into the interface using spaCy. It parses natural text, extracts symptoms, handles greeting intents, and answers queries about precautions and disease descriptions contextually.
- **Weighted ML Predictions:** Uses weights from a symptom-severity mapping database to train a Naive Bayes model (in the web application) and a Random Forest Classifier (in the offline training pipeline).
- **Interactive CLI Predictor:** A simple command-line script to test predictions interactively in the terminal.

---

## 📁 Project Structure

```text
├── app.py                      # Main Flask application and Chatbot backend
├── preprocess_dataset.py       # Script to convert raw symptoms to binary feature format
├── train_model.py              # Script to train and save the Random Forest model
├── predict.py                  # Interactive CLI script for terminal predictions
├── templates/
│   ├── home.html               # Web landing page
│   └── index.html              # Main diagnosis and chatbot interface page
├── static/
│   └── bg.jpg                  # Background image asset
├── dataset.csv                 # Raw symptom-disease dataset
├── processed_dataset.csv       # Preprocessed binary symptom dataset (generated)
├── symptom-severity.csv        # Dataset containing weights for each symptom
├── symptom_description.csv     # Disease descriptions database
├── symptom_precaution.csv      # Precautions to take for each disease
├── model.pkl                   # Saved classifier model (generated)
└── symptoms.pkl                # Saved list of symptoms (generated)
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

### 2. Set Up a Virtual Environment (Recommended)
Navigate to the project root directory and create a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (Command Prompt)
venv\Scripts\activate

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
Install the required packages:

```bash
pip install Flask pandas numpy scikit-learn spacy
```

### 4. Download spaCy Language Model
The chatbot requires spaCy's English language model for tokenization and entity matching:

```bash
python -m spacy download en_core_web_sm
```

---

## ⚙️ How to Run

### Step 1: Preprocess the Dataset
Prepare the symptom list and convert the raw `dataset.csv` into a binary format `processed_dataset.csv`:
```bash
python preprocess_dataset.py
```
*This will also output `symptoms.pkl` containing the sorted list of symptoms.*

### Step 2: Train the Machine Learning Model
Train the Random Forest Classifier on the preprocessed dataset and export the model file:
```bash
python train_model.py
```
*This evaluates model accuracy and outputs `model.pkl` and updates `symptoms.pkl`.*

### Step 3: Launch the Flask Web App
Start the local server:
```bash
python app.py
```
*Access the application by opening [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.*

### Optional: Test via Command Line Interface (CLI)
You can test the trained model interactively in the terminal by running:
```bash
python predict.py
```

---

## 🧠 Behind the Scenes

1. **Preprocessing (`preprocess_dataset.py`):** Converts list-based symptoms in the raw `dataset.csv` into a structured, wide-form binary representation (one column per symptom, 0 if absent, 1 if present).
2. **Model Training (`train_model.py`):** Imports the binary dataset, applies scaling weights based on the gravity of each symptom from `symptom-severity.csv`, and trains a Random Forest Classifier.
3. **Web Server Backend (`app.py`):**
   - Employs a **Multinomial Naive Bayes Model** trained dynamically at startup.
   - The `/chat` endpoint uses NLP techniques via `spaCy` to map human conversational statements into formal symptom tokens. It stores conversation context, allowing the user to ask follow-up questions like *"What precautions should I take?"* or *"What is this?"* based on the latest diagnosed condition.
