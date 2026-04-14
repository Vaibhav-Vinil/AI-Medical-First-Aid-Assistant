import streamlit as st
import sys
import re
from dotenv import load_dotenv
from crew import medical_first_aid_crew

load_dotenv()

st.set_page_config(page_title="AI Medical First Aid Assistant", page_icon="🚑", layout="wide")

class StreamCapture:
    def __init__(self, st_placeholder):
        self.st_placeholder = st_placeholder
        self.buffer = ""
        # Regex to strip out ANSI terminal color codes so they don't show up as garbage text
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def write(self, text):
        clean_text = self.ansi_escape.sub('', text)
        self.buffer += clean_text
        
        # Strip trailing spaces and right-edge characters (│, ╮, ╯) for cleaner UI
        display_lines = []
        for line in self.buffer.split('\n'):
            display_lines.append(line.rstrip(' │╮╯\r'))
            
        self.st_placeholder.text('\n'.join(display_lines))

    def flush(self):
        pass

    def isatty(self):
        return False

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

if submitted:
    if not user_input.strip():
        st.warning("Please enter a medical situation to analyze.")
    else:
        st.info("🔎 Analyzing the symptoms and retrieving medical protocols... Watch the agents work below!")
        
        with st.expander("🤖 Agent Thought Process", expanded=True):
            log_placeholder = st.empty()
            
            # Redirect stdout to our custom stream capture class
            original_stdout = sys.stdout
            sys.stdout = StreamCapture(log_placeholder)
            
            try:
                result = medical_first_aid_crew.kickoff(inputs={"user_input": user_input})
            finally:
                # Always restore the original stdout so we don't break the terminal
                sys.stdout = original_stdout

        st.success("✅ Workflow completed!")

        # Display final result
        st.subheader("📄 Action Plan")
        st.markdown(result.raw if hasattr(result, 'raw') else str(result))
