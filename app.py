import streamlit as st
import sys
import re
import io
import os
import warnings
from dotenv import load_dotenv

# Suppress HuggingFace module warnings
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
warnings.filterwarnings("ignore", message=".*__path__.*")

from crew import medical_first_aid_crew

load_dotenv()

st.set_page_config(page_title="AI Medical First Aid Assistant", page_icon="🚑", layout="wide")

class StreamCapture(io.StringIO):
    def __init__(self, st_placeholder):
        super().__init__()
        self.st_placeholder = st_placeholder
        self.buffer_text = ""
        # Regex to strip out ANSI terminal color codes so they don't show up as garbage text
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def write(self, text):
        clean_text = self.ansi_escape.sub('', text)
        
        # Filter out noisy CrewAIEventsBus sync handler errors
        new_text = ""
        for line in clean_text.splitlines(keepends=True):
            if "[CrewAIEventsBus]" not in line and "Warning: Event pairing mismatch" not in line:
                new_text += line
                
        self.buffer_text += new_text
        
        # Strip trailing spaces and right-edge characters (│, ╮, ╯) for cleaner UI
        display_lines = []
        for line in self.buffer_text.split('\n'):
            if line.strip(): # Optional: prevent huge vertical gaps
                display_lines.append(line.rstrip(' │╮╯\r'))
            
        self.st_placeholder.text('\n'.join(display_lines))
        return len(text)

    def isatty(self):
        return False

# 2-Column Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.title("🚑 AI Medical First Aid Assistant")
    st.markdown(
        "Enter a medical situation or symptom description in plain English. This assistant will help you:\n"
        "- Understand and triage the medical issue\n"
        "- Find applicable first aid protocols\n"
        "- Verify steps using authoritative sources\n"
        "- Present a step-by-step action plan"
    )

    with st.form("medical_form"):
        user_input = st.text_area("📝 Describe the medical issue:", height=150)
        submitted = st.form_submit_button("🔍 Run First Aid Assistant")

    result_container = st.empty()

if submitted:
    if not user_input.strip():
        with col1:
            st.warning("Please enter a medical situation to analyze.")
    else:
        with col1:
            status_msg = st.info("🔎 Analyzing the symptoms and retrieving medical protocols... Watch the agents work on the right!")
            
        with col2:
            st.subheader("🤖 Agent Thought Process")
            with st.container(height=650):
                log_placeholder = st.empty()
            
        # Redirect stdout to our custom stream capture class
        original_stdout = sys.stdout
        sys.stdout = StreamCapture(log_placeholder)
        
        try:
            result = medical_first_aid_crew.kickoff(inputs={"user_input": user_input})
        finally:
            # Always restore the original stdout so we don't break the terminal
            sys.stdout = original_stdout

        with col1:
            status_msg.empty()
            st.success("✅ Workflow completed!")
            st.subheader("📄 Action Plan")
            st.markdown(result.raw if hasattr(result, 'raw') else str(result))
