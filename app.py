import streamlit as st
from groq import Groq
import os
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="CodeRefine - AI Code Review",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #ec4899;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: fadeIn 0.8s ease-in;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .analysis-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #6366f1;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .analysis-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Feature boxes */
    .feature-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border-top: 3px solid #6366f1;
        height: 100%;
    }
    
    .feature-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
        border-top-color: #8b5cf6;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        color: #1f2937;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 0.3rem;
    }
    
    .badge-bug {
        background: #fee2e2;
        color: #dc2626;
    }
    
    .badge-performance {
        background: #fef3c7;
        color: #d97706;
    }
    
    .badge-security {
        background: #dbeafe;
        color: #2563eb;
    }
    
    .badge-best-practice {
        background: #d1fae5;
        color: #059669;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 8px;
        border-left: 4px solid #6366f1;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Text area */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        font-family: 'Courier New', monospace;
    }
    
    .stTextArea textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Metrics */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
    }
    
    .metric-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

def initialize_groq_client(api_key):
    """Initialize Groq client with API key"""
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {str(e)}")
        return None

def analyze_code(client, code, analysis_type):
    """Analyze code using Groq API"""
    
    prompts = {
        "comprehensive": """You are an expert code reviewer. Analyze the following code comprehensively and provide:

1. **Bug Detection**: Identify any bugs, errors, or potential runtime issues
2. **Performance Issues**: Point out performance bottlenecks and inefficiencies
3. **Security Vulnerabilities**: Detect security risks and vulnerabilities
4. **Best Practice Violations**: Identify violations of coding standards and best practices
5. **Optimized Code**: Provide a complete rewritten version of the code with all improvements

Format your response as:
## 🐛 Bugs Detected
[List bugs with line numbers if applicable]

## ⚡ Performance Issues
[List performance concerns]

## 🔒 Security Concerns
[List security vulnerabilities]

## ✨ Best Practice Recommendations
[List best practice violations]

## 🚀 Optimized Code
```
[Provide the complete optimized code]
```

## 📝 Summary
[Brief summary of changes made]

Code to analyze:
```
{code}
```""",
        
        "bugs": """You are a bug detection expert. Analyze the following code and identify all bugs, errors, and potential runtime issues. For each bug:
- Describe the issue
- Explain why it's a problem
- Suggest how to fix it

Code:
```
{code}
```""",
        
        "performance": """You are a performance optimization expert. Analyze the following code for performance issues:
- Identify bottlenecks
- Suggest algorithmic improvements
- Recommend better data structures
- Point out unnecessary computations

Code:
```
{code}
```""",
        
        "security": """You are a security expert. Analyze the following code for security vulnerabilities:
- Input validation issues
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization flaws
- Data exposure risks

Code:
```
{code}
```""",
        
        "best_practices": """You are a code quality expert. Review the following code for best practice violations:
- Code organization and structure
- Naming conventions
- Code readability
- Documentation
- Error handling
- Design patterns

Code:
```
{code}
```""",
        
        "rewrite": """You are an expert programmer. Rewrite the following code to be:
- Bug-free
- Performant
- Secure
- Following best practices
- Well-documented

Provide only the optimized code with inline comments explaining key improvements.

Original code:
```
{code}
```"""
    }
    
    try:
        prompt = prompts[analysis_type].format(code=code)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are CodeRefine, an expert AI code reviewer specializing in bug detection, performance optimization, security analysis, and code quality improvement."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=4000,
        )
        
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        return f"Error during analysis: {str(e)}"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 CodeRefine</h1>
        <p>Generative AI-Powered Code Review & Optimization Engine</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Enter your Groq API key to enable code analysis"
        )
        
        if api_key:
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Please enter your Groq API Key")
        
        st.markdown("---")
        
        # Analysis type selection
        st.markdown("### 🎯 Analysis Type")
        analysis_type = st.selectbox(
            "Select analysis mode",
            [
                "comprehensive",
                "bugs",
                "performance",
                "security",
                "best_practices",
                "rewrite"
            ],
            format_func=lambda x: {
                "comprehensive": "🔬 Comprehensive Review",
                "bugs": "🐛 Bug Detection",
                "performance": "⚡ Performance Analysis",
                "security": "🔒 Security Audit",
                "best_practices": "✨ Best Practices",
                "rewrite": "🚀 Code Rewrite"
            }[x]
        )
        
        st.markdown("---")
        
        # Features showcase
        st.markdown("### ✨ Features")
        st.markdown("""
        - 🐛 **Bug Detection**
        - ⚡ **Performance Optimization**
        - 🔒 **Security Analysis**
        - ✨ **Best Practice Checks**
        - 🚀 **Code Rewriting**
        """)
        
        st.markdown("---")
        
        # Statistics
        if st.session_state.analysis_history:
            st.markdown("### 📊 Statistics")
            st.metric("Total Analyses", len(st.session_state.analysis_history))
    
    # Main content area
    col1, col2, col3, col4, col5 = st.columns(5)
    
    features = [
        ("🐛", "Bug Detection", "Identify errors and runtime issues"),
        ("⚡", "Performance", "Optimize code efficiency"),
        ("🔒", "Security", "Detect vulnerabilities"),
        ("✨", "Best Practices", "Follow coding standards"),
        ("🚀", "Rewrite", "Get optimized code")
    ]
    
    for col, (icon, title, desc) in zip([col1, col2, col3, col4, col5], features):
        with col:
            st.markdown(f"""
            <div class="feature-box">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Code input section
    st.markdown("### 📝 Enter Your Code")
    
    # Language selection
    language = st.selectbox(
        "Programming Language",
        ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Ruby", "PHP", "TypeScript", "Other"],
        help="Select the programming language of your code"
    )
    
    # Code input
    code_input = st.text_area(
        "Paste your code here",
        height=300,
        placeholder="# Paste your code here...\n\ndef example_function():\n    pass",
        help="Enter the code you want to analyze"
    )
    
    # Analyze button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button("🔍 Analyze Code", use_container_width=True)
    
    # Analysis section
    if analyze_button:
        if not api_key:
            st.error("❌ Please enter your Groq API key in the sidebar")
        elif not code_input.strip():
            st.error("❌ Please enter some code to analyze")
        else:
            # Initialize client
            client = initialize_groq_client(api_key)
            
            if client:
                with st.spinner("🔄 Analyzing your code... This may take a moment."):
                    # Perform analysis
                    result = analyze_code(client, code_input, analysis_type)
                    
                    # Store in history
                    st.session_state.analysis_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "language": language,
                        "type": analysis_type,
                        "code_length": len(code_input)
                    })
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("## 📊 Analysis Results")
                    
                    # Create tabs for better organization
                    tab1, tab2 = st.tabs(["📋 Analysis Report", "💻 Original Code"])
                    
                    with tab1:
                        st.markdown(f"""
                        <div class="analysis-card">
                            <strong>Language:</strong> {language} | 
                            <strong>Analysis Type:</strong> {analysis_type.replace('_', ' ').title()} | 
                            <strong>Code Lines:</strong> {len(code_input.splitlines())}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(result)
                        
                        # Download button for results
                        st.download_button(
                            label="📥 Download Analysis Report",
                            data=result,
                            file_name=f"coderefine_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                    
                    with tab2:
                        st.code(code_input, language=language.lower())
                    
                    st.success("✅ Analysis completed successfully!")
    
    # Analysis history
    if st.session_state.analysis_history:
        st.markdown("---")
        st.markdown("## 📜 Recent Analyses")
        
        # Display last 5 analyses
        for i, analysis in enumerate(reversed(st.session_state.analysis_history[-5:])):
            with st.expander(f"Analysis {len(st.session_state.analysis_history) - i} - {analysis['timestamp']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Language:** {analysis['language']}")
                with col2:
                    st.markdown(f"**Type:** {analysis['type'].replace('_', ' ').title()}")
                with col3:
                    st.markdown(f"**Code Length:** {analysis['code_length']} chars")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem;">
        <p><strong>CodeRefine</strong> - Powered by Groq AI & LLaMA 3.1</p>
        <p style="font-size: 0.9rem;">Accelerate development with AI-powered code review</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
