# 🔍 CodeRefine - AI-Powered Code Review & Optimization Engine

CodeRefine is a Generative AI-powered tool that analyzes source code to identify bugs, performance issues, security vulnerabilities, and best-practice violations. It provides optimized code rewrites to help developers improve quality and accelerate development cycles.

## ✨ Features

- 🐛 **Automated Bug Detection** - Identifies errors and potential runtime issues
- ⚡ **Performance Optimization** - Detects bottlenecks and suggests improvements
- 🔒 **Security Analysis** - Finds vulnerabilities and security risks
- ✨ **Best Practice Checks** - Ensures code follows industry standards
- 🚀 **Code Rewriting** - Generates optimized, production-ready code
- 📊 **Analysis History** - Track your code reviews over time

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd c:\Users\Dharani\OneDrive\Desktop\Coderefine
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Enter your Groq API key** in the sidebar when the app opens

## 📖 How to Use

1. **Enter your Groq API Key** in the sidebar
2. **Select an analysis type:**
   - 🔬 Comprehensive Review - Full analysis with all checks
   - 🐛 Bug Detection - Focus on bugs and errors
   - ⚡ Performance Analysis - Optimize code performance
   - 🔒 Security Audit - Find security vulnerabilities
   - ✨ Best Practices - Check coding standards
   - 🚀 Code Rewrite - Get optimized code

3. **Select your programming language**
4. **Paste your code** in the text area
5. **Click "Analyze Code"** and wait for results
6. **Review the analysis** and download the report if needed

## 🎨 Features Showcase

### Professional UI
- Modern gradient design with smooth animations
- Responsive layout that works on all screen sizes
- Interactive hover effects and transitions
- Clean, organized presentation of results

### Multiple Analysis Modes
- Comprehensive reviews covering all aspects
- Specialized analysis for specific concerns
- Detailed explanations and recommendations
- Complete code rewrites with improvements

### Analysis History
- Track all your code reviews
- View statistics and metrics
- Easy access to recent analyses

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **AI Model:** LLaMA 3.1 8B (via Groq)
- **Language:** Python 3.8+

## 📝 Example Usage

```python
# Paste code like this in the app:
def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total

# CodeRefine will analyze and suggest:
# - Performance improvements (use sum() or list comprehension)
# - Best practices (more Pythonic code)
# - Optimized rewrite
```

## 🔑 Getting a Groq API Key

1. Visit [Groq Console](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste it into CodeRefine

## 🤝 Support

For issues or questions, please check:
- Ensure your Groq API key is valid
- Verify all dependencies are installed
- Check that you're using Python 3.8+

## 📄 License

This project is created for educational and development purposes.

---

**Built with ❤️ using Streamlit and Groq AI**
