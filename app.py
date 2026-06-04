from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import numpy as np
import random
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
import spacy
from spacy.matcher import PhraseMatcher

app = Flask(__name__)

try:
    dataset = pd.read_csv('dataset.csv')
    symptom_severity = pd.read_csv('symptom-severity.csv')
    desc_df = pd.read_csv('symptom_description.csv')
    prec_df = pd.read_csv('symptom_precaution.csv')

    # Clean column names
    dataset.columns = dataset.columns.str.strip()
    symptom_severity.columns = symptom_severity.columns.str.strip()
    desc_df.columns = desc_df.columns.str.strip()
    prec_df.columns = prec_df.columns.str.strip()
except FileNotFoundError:
    print("Warning: Data files not found. Ensure dataset.csv, symptom-severity.csv, etc., are present.")
    # Initialize empty dataframes to prevent crashes
    dataset, symptom_severity, desc_df, prec_df = [pd.DataFrame() for _ in range(4)]


if not dataset.empty and 'Disease' in dataset.columns and len(dataset.columns) > 1 and not symptom_severity.empty:
    X = dataset.iloc[:, 1:].fillna('')
    y = dataset['Disease']

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Map each symptom to an index
    symptom_severity['Symptom'] = symptom_severity['Symptom'].str.strip().str.replace('_', ' ')
    symptom_index = {symptom: i for i, symptom in enumerate(symptom_severity['Symptom'])}
    
    # Prepare training data with weights
    X_train = []
    for i in range(len(X)):
        row = [0] * len(symptom_index)
        for symptom in X.iloc[i]:
            symptom = symptom.strip().replace('_', ' ')
            if symptom in symptom_index:
                weight = symptom_severity.loc[
                    symptom_severity['Symptom'] == symptom, 'weight'
                ].values[0]
                row[symptom_index[symptom]] = weight
        X_train.append(row)
    X_train = np.array(X_train)

    # Train Naive Bayes model
    model = MultinomialNB()
    model.fit(X_train, y_encoded)
    
    # Global symptom list for UI
    ALL_SYMPTOMS = list(symptom_severity['Symptom'])
    # Set of all symptoms for NLP matching (lowercase)
    SYMPTOMS_SET = set([s.lower() for s in ALL_SYMPTOMS])
else:
    # Handle case where data loading failed
    model = None
    ALL_SYMPTOMS = []
    SYMPTOMS_SET = set()

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spaCy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'")
    nlp = None

chat_context = {"last_disease": None, "current_symptoms": set()}

def extract_symptoms(text, symptoms_set):
    """Uses lemmatization and noun chunking to better extract symptoms."""
    if not nlp: return set()

    doc = nlp(text.lower())
    matched_symptoms = set()
    
    # 1. Check tokens and lemmas
    tokens = [t.lemma_ for t in doc if not t.is_stop and not t.is_punct]
    
    # 2. Check Noun Chunks (for multi-word symptoms like 'high fever')
    phrases = [chunk.text for chunk in doc.noun_chunks]

    for symptom in symptoms_set:
        # Check against cleaned tokens
        if any(token in symptom or symptom in token for token in tokens):
            matched_symptoms.add(symptom)
        # Check against noun phrases
        elif any(symptom in phrase for phrase in phrases):
             matched_symptoms.add(symptom)

    return matched_symptoms

def get_intent(text):
    """Detects primary user intent."""
    intents = {
        "precaution": ["precaution", "prevent", "avoid", "care", "how to stop"],
        "description": ["what is", "explain", "about", "information", "describe"],
        "symptom_query": ["symptom", "sign", "feel", "what are the signs", "have", "am feeling"],
        "greeting": ["hi", "hello", "hey", "good morning", "good evening"],
        "thanks": ["thank you", "thanks", "tks"],
        "reset": ["reset", "start over", "clear", "new diagnosis"],
    }
    
    text = text.lower()
    for key, words in intents.items():
        if any(w in text for w in words):
            return key
    
    # Default to symptom query if user lists symptoms but no specific intent keyword
    if len(extract_symptoms(text, SYMPTOMS_SET)) > 0:
        return "symptom_query"
        
    return None

def format_diagnosis(disease, confidence, desc_df, prec_df):
    """Returns core diagnosis data as a dictionary."""
    desc = desc_df.loc[desc_df['Disease'] == disease, 'Description'].values
    precautions = prec_df.loc[prec_df['Disease'] == disease].values

    desc_text = desc[0] if len(desc) > 0 else "General condition based on symptoms."
    precaution_list = [str(p) for p in precautions[0][1:] if str(p) != 'nan']
    
    return {
        "disease": disease,
        "confidence": confidence,
        "description": desc_text,
        "precautions": precaution_list
    }

@app.route("/")
def landing():
    return render_template("home.html")

@app.route("/diagnosis", methods=["GET", "POST"])
def index():
    symptoms = ALL_SYMPTOMS
    top_predictions = None

    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")

        if selected_symptoms and model:
            # The diagnosis logic from the original file (kept for the main diagnosis form)
            input_data = [0] * len(symptom_index)
            for s in selected_symptoms:
                s_cleaned = s.strip().replace('_', ' ')
                if s_cleaned in symptom_index:
                    input_data[symptom_index[s_cleaned]] = symptom_severity.loc[
                        symptom_severity['Symptom'] == s_cleaned, 'weight'
                    ].values[0]

            input_data = np.array(input_data).reshape(1, -1)
            pred_probs = model.predict_proba(input_data)[0]

            valid_indices = [i for i, p in enumerate(pred_probs) if p > 0]
            top_indices = sorted(valid_indices, key=lambda i: pred_probs[i], reverse=True)[:5]

            top_predictions = []
            for idx in top_indices:
                disease = le.inverse_transform([idx])[0]
                confidence = round(pred_probs[idx] * 100, 2)
                if confidence <= 0:
                    continue

                desc = desc_df.loc[desc_df['Disease'] == disease, 'Description'].values
                precautions = prec_df.loc[prec_df['Disease'] == disease].values

                desc_text = (
                    desc[0] if len(desc) > 0
                    else f"This condition shows symptoms like {', '.join(selected_symptoms)}."
                )
                precaution_text = (
                    ', '.join([str(p) for p in precautions[0][1:] if str(p) != 'nan'])
                    if len(precautions) > 0 else "No specific precautions found."
                )

                top_predictions.append({
                    "disease": disease,
                    "confidence": confidence,
                    "description": desc_text,
                    "precaution": precaution_text
                })

    return render_template("index.html", symptoms=symptoms, top_predictions=top_predictions)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    global chat_context

    intent = get_intent(user_msg)
    user_msg_lower = user_msg.lower()
    current_symptoms = chat_context["current_symptoms"]

    if intent == "greeting":
        return jsonify({"reply": random.choice([
            "Hello! I'm your AI Medical Assistant. How are you feeling today?",
            "Hi there! Tell me what's bothering you, or ask about a specific disease.",
            "Hey! You can start by listing your symptoms, like 'I have a high fever and muscle pain'."
        ])})
    
    if intent == "thanks":
        return jsonify({"reply": random.choice([
            "You're very welcome! Feel free to ask anything else.",
            "Glad I could help!",
            "Anytime. Take care!"
        ])})
        
    if intent == "reset":
        chat_context["last_disease"] = None
        chat_context["current_symptoms"] = set()
        return jsonify({"reply": "I've cleared our conversation context. Please tell me your symptoms for a new diagnosis!"})

    diagnosis_trigger_words = ["diagnose", "run analysis", "what is it", "tell me now", "calculate"]
    confirmation_words = ["yes", "ok", "sure", "that's it", "run", "go"] 
    
    is_diagnosis_command = (
        any(w in user_msg_lower for w in diagnosis_trigger_words) or
        (len(current_symptoms) > 0 and any(w in user_msg_lower.split() for w in confirmation_words))
    )
    
    # If the user issues a command AND we have symptoms, run diagnosis now!
    if is_diagnosis_command and len(current_symptoms) > 0 and model:
        # Diagnosis Logic Start
        input_data = [0] * len(symptom_index)
        symptom_names_for_model = [s for s in current_symptoms if s in symptom_index]
        
        if not symptom_names_for_model:
            chat_context["current_symptoms"] = set()
            return jsonify({"reply": "I apologize, I didn't recognize any specific symptoms in your messages. Could you try listing them clearly?"})
        
        for s in symptom_names_for_model:
            weight = symptom_severity.loc[symptom_severity['Symptom'] == s, 'weight'].values[0]
            input_data[symptom_index[s]] = weight
            
        input_data = np.array(input_data).reshape(1, -1)
        pred_probs = model.predict_proba(input_data)[0]

        valid_indices = [i for i, p in enumerate(pred_probs) if p > 0]
        top_indices = sorted(valid_indices, key=lambda i: pred_probs[i], reverse=True)[:3]
        
        results = []
        
        if not top_indices:
             chat_context["current_symptoms"] = set()
             chat_context["last_disease"] = None
             return jsonify({"reply": "I couldn't find a strong match for those symptoms in my database. Please seek professional medical advice."})


        # Generate detailed, formatted dictionary for top 3
        for idx in top_indices:
            disease = le.inverse_transform([idx])[0]
            confidence = round(pred_probs[idx] * 100, 2)
            if confidence > 0:
                results.append(format_diagnosis(disease, confidence, desc_df, prec_df))

        top_result = results[0]
        summary_lines = []
        
        summary_lines.append(
            f"Based on your symptoms, the most likely diagnosis is {top_result['disease']} with {top_result['confidence']}% confidence. "
        )
        
        # 2. Description
        summary_lines.append(f"It is described as: {top_result['description']}.")

        # 3. Precautions
        if top_result['precautions']:
            prec_str = ", ".join(top_result['precautions'])
            summary_lines.append(f"Recommended precautions include: {prec_str}.")
        
        # 4. Secondary predictions (if any)
        if len(results) > 1:
            secondary_diseases = [f"{r['disease']} ({r['confidence']}%)" for r in results[1:]]
            summary_lines.append(
                f"Secondary possibilities are {', '.join(secondary_diseases)}."
            )
            
        # 5. Final message and disclaimer
        summary_lines.append(
            "\nPlease remember I am an AI and this is not a professional diagnosis. Consult a doctor for confirmation."
        )
        
        chat_context["last_disease"] = top_result['disease']
        chat_context["current_symptoms"] = set()
        
        # Join lines into a single, clean paragraph/summary
        final_reply = " ".join(summary_lines)
        return jsonify({"reply": final_reply.replace('\n', '<br>')})
        # Diagnosis Logic End

    last_disease = chat_context.get("last_disease")
    
    if last_disease and (intent == "precaution" or intent == "description"):
        
        # Lookup information for the last disease
        if intent == "precaution":
            precautions = prec_df.loc[prec_df['Disease'] == last_disease].values
            precaution_list = [str(p) for p in precautions[0][1:] if str(p) != 'nan']

            if precaution_list:
                # Removed Markdown and newline formatting
                reply = f"For {last_disease}, you should take these precautions: " + ", ".join(precaution_list) + "."
            else:
                reply = f"I don't have specific precautions for {last_disease} in my current database, but general rest and hydration are always advised."
                
        elif intent == "description":
            desc = desc_df.loc[desc_df['Disease'] == last_disease, 'Description'].values
            desc_text = desc[0] if len(desc) > 0 else f"I couldn't find a detailed description for {last_disease}."
            # Removed Markdown
            reply = f"{last_disease} is typically described as: {desc_text}"
            
        return jsonify({"reply": reply})

    new_symptoms = extract_symptoms(user_msg, SYMPTOMS_SET)
    
    # If new symptoms are found, add them to the context
    if new_symptoms:
        chat_context["current_symptoms"].update(new_symptoms)
        
        # If the context was reset (new diagnosis started), clear the last disease
        if chat_context["last_disease"] is not None:
             chat_context["last_disease"] = None
        
        # Acknowledge the symptoms found
        symptom_list = ", ".join([s.title() for s in new_symptoms])
        all_current_symptoms = ', '.join([s.title() for s in chat_context['current_symptoms']])

        if len(chat_context["current_symptoms"]) > len(new_symptoms):
            # User added to existing symptoms
            ack_msg = f"Got it. I've added {symptom_list} to your list. Your current symptoms are: {all_current_symptoms}. Shall I run the diagnosis now?"
        else:
            # First set of symptoms
            ack_msg = f"Thank you for sharing. I've noted down {symptom_list}. Do you have any other symptoms to add, or would you like me to run the diagnosis?"
        
        return jsonify({"reply": ack_msg})

    fallback = [
        "I'm sorry, I couldn't fully understand that. Could you please rephrase, or list your symptoms clearly?",
        "Try telling me a specific symptom (like 'dizziness') or asking about a disease (like 'What are the precautions for Malaria?').",
        "I need a clear symptom or question. For a new diagnosis, list your symptoms again or type 'reset'."
    ]
    return jsonify({"reply": random.choice(fallback)})

if __name__ == "__main__":
    app.run(debug=True)
