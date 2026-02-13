# 🚀 Code Refine - AI Code Analysis Tool

Code Refine is a powerful, local-first AI tool designed to analyze source code for bugs, performance issues, security risks, and best practices. It features a modern integrated developer environment (IDE) feel and provides actionable insights and optimized code rewrites.

## ✨ Features

- **Automated Code Review**: Detects bugs, style issues, and logic errors.
- **Security Scanning**: Identifies potential vulnerabilities like SQL injection and hardcoded secrets.
- **Performance Optimization**: Suggests improvements for faster, more efficient code.
- **AI Code Rewriting**: Generates optimized, cleaner versions of your code.
- **Dual AI Engine**:
  - **Groq AI (Cloud)**: Fast, high-quality analysis using the Groq API.
  - **Mock AI (Local)**: Instant, simulation mode for offline use or testing without keys.
- **PDF Reports**: specific analysis reports can be downloaded as PDF.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Engine**: Groq (Cloud), Custom Mock Engine (Local)
- **Editor**: Streamlit Ace (Monaco-like experience)
- **Reporting**: FPDF

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1.  Clone the repository or download the source code.
2.  Navigate to the project directory:
    ```bash
    cd coderefine
    ```
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Run the application using Streamlit:

```bash
python -m streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## ⚙️ Configuration

- **API Key**: The application comes with a pre-configured Groq API key. You can update it in `app.py` or use the Mock AI mode from the sidebar.
- **Mock Mode**: Toggle "Use Mock AI" in the sidebar to switch to the offline simulation engine.

## 📝 License

This project is open-source and available for all developers.
