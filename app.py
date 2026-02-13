import streamlit as st
import os
import json
import time
from groq import Groq
from fpdf import FPDF
from streamlit_ace import st_ace
from dotenv import load_dotenv

# --- Configuration & Constants ---
load_dotenv()
APP_NAME = "Code Refine"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEFAULT_THEME = "monokai"
DEFAULT_LANGUAGE = "python"

# --- Mock AI Engine ---
class MockAIEngine:
    @staticmethod
    def analyze_code(code, language):
        time.sleep(2)  # Simulate network delay
        return {
            "bugs": [
                f"Potential null reference in {language} code at line 5",
                "Syntax warning: unused variable 'x'"
            ],
            "performanceIssues": [
                "Detected inefficient loop structure. Consider using list comprehensions (Python) or map/filter (JS).",
                "Redundant database query inside loop."
            ],
            "securityRisks": [
                "Potential SQL Injection vulnerability detected in query string.",
                "Hardcoded secret key found."
            ],
            "suggestions": [
                "Use meaningful variable names.",
                "Add docstrings to functions."
            ],
            "rewrittenCode": f"# Optimized {language} code\n\ndef optimized_function():\n    # Secure and fast implementation\n    pass\n" + code
        }

# --- Groq AI Integration ---
class GroqAIEngine:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def analyze_code(self, code, language):
        prompt = f"""
        Analyze the following {language} code for bugs, performance issues, security risks, and best practices.
        Also provide a rewritten, optimized version of the code.
        
        Return the response strictly in the following JSON format:
        {{
            "bugs": ["list of bugs"],
            "performanceIssues": ["list of performance issues"],
            "securityRisks": ["list of security risks"],
            "suggestions": ["list of general suggestions"],
            "rewrittenCode": "the full optimized code string"
        }}

        Code to analyze:
        {code}
        """
        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert senior software engineer and code auditor. You output only JSON."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            st.error(f"AI Engine Error: {e}")
            return None

# --- PDF Report Generator ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Code Refine - Analysis Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_pdf(analysis_result):
    pdf = PDFReport()
    pdf.add_page()
    
    for category in ["bugs", "performanceIssues", "securityRisks", "suggestions"]:
        pdf.chapter_title(category.replace("Is", " Is").capitalize())
        items = analysis_result.get(category, [])
        if items:
            for item in items:
                 pdf.chapter_body(f"- {item}")
        else:
            pdf.chapter_body("No issues found.")

    pdf.add_page()
    pdf.chapter_title("Rewritten Code")
    pdf.set_font("Courier", "", 10)
    pdf.multi_cell(0, 5, analysis_result.get("rewrittenCode", ""))
    
    return pdf.output(dest='S').encode('latin-1')

# --- Main App Logic ---
def main():
    st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🚀")

    # Custom CSS for "Mental" Aesthetics
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            font-family: 'Segoe UI', sans-serif;
            color: #4CAF50;
        }
        .report-card {
            background-color: #262730;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 10px;
            border-left: 5px solid #4CAF50;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title(f"🚀 {APP_NAME}")
    st.markdown("### AI-Powered Code Analysis & Optimization Tool")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        language = st.selectbox("Language", ["python", "javascript", "java", "cpp", "go", "rust"], index=0)
        use_mock = st.toggle("Use Mock AI (Offline Mode)", value=False)
        st.divider()
        st.markdown("**Features:**")
        st.markdown("- 🐞 Bug Detection")
        st.markdown("- ⚡ Performance Optimization")
        st.markdown("- 🔒 Security Scanning")
        st.markdown("- ✨ Code Rewriting")

    # Main Layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📝 Source Code")
        # Editor
        code_input = st_ace(
            placeholder="Paste your code here...",
            language=language,
            theme=DEFAULT_THEME,
            key="code_editor",
            height=600,
            font_size=14
        )
        
        analyze_btn = st.button("🔍 Analyze Code", type="primary")

    # Analysis Logic
    if analyze_btn:
        if not code_input:
            st.warning("Please enter some code to analyze.")
        else:
            with st.spinner("🤖 Analyzing code..."):
                engine = None
                if use_mock:
                    engine = MockAIEngine()
                else:
                    engine = GroqAIEngine(GROQ_API_KEY)

                results = engine.analyze_code(code_input, language)

                if results:
                    st.session_state['results'] = results
                    st.success("Analysis Complete!")
                else:
                    st.error("Analysis failed. Please try again or switch to Mock AI.")

    # Results Display
    with col2:
        st.subheader("📊 Analysis Results")
        
        if 'results' in st.session_state:
            results = st.session_state['results']
            
            # Tabs for different categories
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["🐞 Bugs", "⚡ Performance", "🔒 Security", "💡 Suggestions", "✨ Rewrite"])
            
            with tab1:
                if results['bugs']:
                    for bug in results['bugs']:
                        st.error(bug, icon="🐞")
                else:
                    st.success("No bugs detected!", icon="✅")

            with tab2:
                if results['performanceIssues']:
                    for issue in results['performanceIssues']:
                        st.warning(issue, icon="⚡")
                else:
                    st.success("Performance looks good!", icon="✅")

            with tab3:
                if results['securityRisks']:
                    for risk in results['securityRisks']:
                        st.error(risk, icon="🔒")
                else:
                    st.success("No security risks found!", icon="✅")
            
            with tab4:
                 if results['suggestions']:
                    for suggestion in results['suggestions']:
                        st.info(suggestion, icon="💡")
                 else:
                    st.info("No suggestions available.")

            with tab5:
                st.code(results['rewrittenCode'], language=language)
            
            st.divider()
            
            # PDF Download
            try:
                pdf_bytes = generate_pdf(results)
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name="code_analysis_report.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Could not generate PDF: {e}")

        else:
            st.info("Run analysis to see results here.")

if __name__ == "__main__":
    main()
