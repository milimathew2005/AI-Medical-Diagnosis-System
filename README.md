# AI Debate Arena

An interactive AI-powered debate platform where two AI agents engage in structured debates on user-provided topics. The system generates arguments, counterarguments, and rebuttals while presenting the debate in a user-friendly web interface. Users can observe how different AI perspectives reason, challenge each other, and arrive at conclusions.

> [!WARNING]
> **Educational Disclaimer:** This application is designed for educational, research, and demonstration purposes. AI-generated arguments may contain inaccuracies, biases, or outdated information. Users should independently verify critical information before relying on it.

---

## 🚀 Features

* **AI vs AI Debates:** Two AI agents debate opposing viewpoints on a given topic.
* **Automated Argument Generation:** AI agents generate opening statements, rebuttals, and closing remarks.
* **Structured Debate Flow:** Multiple rounds of argument exchange for deeper discussion.
* **Real-Time Debate Visualization:** Clean web interface for viewing debate progression.
* **Firebase Integration:** Stores debate history and user interactions.
* **Cloud-Powered AI Processing:** Uses Google Cloud AI services for generating debate responses.
* **Topic Flexibility:** Supports debates on technology, science, ethics, education, business, and more.

---

## 📁 Project Structure

```text
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Application pages
│   │   ├── services/          # API communication services
│   │   └── App.js             # Main application component
│   └── package.json
│
├── backend/
│   ├── debate_engine.py       # AI debate orchestration logic
│   ├── prompts.py             # AI prompt templates
│   ├── firebase_service.py    # Firebase integration
│   ├── config.py              # Configuration settings
│   └── app.py                 # Backend API server
│
├── firebase/
│   └── firestore.rules        # Firestore security rules
│
├── docs/
│   └── architecture.md        # System design documentation
│
├── requirements.txt
├── README.md
└── .env
```

---

## 🛠️ Technologies Used

### Frontend

* React.js
* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask

### AI & Cloud Services

* Google Gemini API
* Google Cloud Platform (GCP)

### Database

* Firebase Firestore

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-debate-arena
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
```

### 6. Start the Backend Server

```bash
python app.py
```

### 7. Start the Frontend

```bash
cd frontend
npm start
```

The application will be available at:

```text
http://localhost:3000
```

---

## 🎯 How It Works

### Step 1: Topic Submission

The user enters a debate topic through the web interface.

### Step 2: Position Assignment

The system assigns two AI agents opposing viewpoints:

* AI Agent A → Supports the topic
* AI Agent B → Opposes the topic

### Step 3: Debate Execution

The debate engine manages multiple rounds:

1. Opening Statements
2. Rebuttal Round
3. Counterarguments
4. Closing Statements

### Step 4: Result Presentation

The complete debate is displayed in an organized format, allowing users to analyze both perspectives.

---

## 🧠 System Architecture

### Frontend Layer

Handles user interaction, debate visualization, and API communication.

### Backend Layer

Coordinates debate flow, manages prompts, and communicates with AI services.

### AI Layer

Uses Google Gemini models to generate context-aware arguments and rebuttals.

### Database Layer

Stores debate history, topics, timestamps, and generated responses using Firebase Firestore.

---

## 🔥 Future Enhancements

* Debate winner prediction using AI evaluation.
* User voting system.
* Multi-agent debates involving more than two AI participants.
* Voice-enabled debates using speech synthesis.
* Real-time collaborative debate rooms.
* Analytics dashboard for debate quality assessment.
* Export debates as PDF or text reports.

---

## 📊 Educational Applications

This project can be used for:

* Critical thinking development
* Argument analysis
* AI reasoning research
* Classroom discussions
* Public speaking preparation
* Decision-making support

---

## 👨‍💻 Authors

Developed as a B.Tech Artificial Intelligence Engineering project demonstrating the integration of Generative AI, Cloud Computing, and Modern Web Technologies.

---

## 📄 License

This project is intended for educational and academic purposes.
