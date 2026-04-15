import streamlit as st
import streamlit.components.v1 as components
import sys
import re
import io
import os
import warnings
from dotenv import load_dotenv

# Suppress HuggingFace module warnings
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
warnings.filterwarnings("ignore", message=".*__path__.*")
warnings.filterwarnings("ignore", message=".*unauthenticated requests.*")

from crew import medical_first_aid_crew

load_dotenv()

st.set_page_config(page_title="AI Medical First Aid Assistant", page_icon="🚑", layout="wide")

_SS_PLAN = "first_aid_plan"
_SS_LOGS = "first_aid_logs"
_SS_ERR = "first_aid_error"
_SS_SCROLL = "_scroll_to_action_plan"


def _init_session_state() -> None:
    if _SS_PLAN not in st.session_state:
        st.session_state[_SS_PLAN] = None
    if _SS_LOGS not in st.session_state:
        st.session_state[_SS_LOGS] = None
    if _SS_ERR not in st.session_state:
        st.session_state[_SS_ERR] = None
    if _SS_SCROLL not in st.session_state:
        st.session_state[_SS_SCROLL] = False


_init_session_state()


def _scroll_action_plan_into_view() -> None:
    """Scroll main page so the Action Plan (anchor) is visible after a new run."""
    components.html(
        """
        <script>
        (function () {
            const doc = window.parent.document;
            const el = doc.getElementById("streamlit-action-plan-anchor");
            if (el) {
                el.scrollIntoView({ behavior: "smooth", block: "start" });
                return;
            }
            const main = doc.querySelector('[data-testid="stAppViewContainer"]')
                || doc.querySelector("section.main");
            if (main) {
                main.scrollTo({ top: main.scrollHeight, behavior: "smooth" });
            }
        })();
        </script>
        """,
        height=0,
        width=0,
    )


class TeeStdout:
    """Mirror writes to the real console and another stream (e.g. Streamlit capture)."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, text):
        for s in self.streams:
            try:
                s.write(text)
            except Exception:
                pass
        return len(text)

    def flush(self):
        for s in self.streams:
            if hasattr(s, "flush"):
                try:
                    s.flush()
                except Exception:
                    pass

    def isatty(self):
        return getattr(self.streams[0], "isatty", lambda: False)()


class StreamCapture(io.StringIO):
    def __init__(self, st_placeholder):
        super().__init__()
        self.st_placeholder = st_placeholder
        self.buffer_text = ""
        self.ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def write(self, text):
        clean_text = self.ansi_escape.sub("", text)
        new_text = ""
        for line in clean_text.splitlines(keepends=True):
            if "[CrewAIEventsBus]" in line or "Warning: Event pairing mismatch" in line:
                continue
            # Noisy internal event-bus pairing warnings (not useful in the UI)
            if "(expected '" in line and line.strip().startswith("'"):
                continue
            new_text += line

        self.buffer_text += new_text

        if new_text:
            display_lines = []
            for line in self.buffer_text.split("\n"):
                if line.strip():
                    display_lines.append(line.rstrip(" │╮╯\r"))
            self.st_placeholder.text("\n".join(display_lines))
        return len(text)

    def isatty(self):
        return False


col1, col2 = st.columns([1, 1])

with col2:
    st.subheader("🤖 Agent Thought Process")
    with st.container(height=650):
        log_placeholder = st.empty()
        if st.session_state[_SS_LOGS]:
            log_placeholder.text(st.session_state[_SS_LOGS])

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

    if st.button("Clear results", type="secondary"):
        st.session_state[_SS_PLAN] = None
        st.session_state[_SS_LOGS] = None
        st.session_state[_SS_ERR] = None
        st.session_state[_SS_SCROLL] = False
        st.rerun()

    if submitted:
        if not user_input.strip():
            st.warning("Please enter a medical situation to analyze.")
        else:
            st.session_state[_SS_ERR] = None
            prior_stdout = sys.stdout
            # Tee: real console (for the terminal where you ran `streamlit run`) + Streamlit capture.
            console_out = getattr(sys, "__stdout__", None) or prior_stdout
            capture = StreamCapture(log_placeholder)
            sys.stdout = TeeStdout(console_out, capture)
            try:
                with st.spinner("Analyzing… running the medical first-aid crew (this may take a minute)."):
                    result = medical_first_aid_crew.kickoff(inputs={"user_input": user_input})
                plan = result.raw if hasattr(result, "raw") else str(result)
                st.session_state[_SS_PLAN] = plan
                st.session_state[_SS_LOGS] = capture.buffer_text
                st.session_state[_SS_SCROLL] = True
            except Exception as e:
                st.session_state[_SS_PLAN] = None
                st.session_state[_SS_LOGS] = capture.buffer_text
                st.session_state[_SS_ERR] = str(e)
            finally:
                sys.stdout = prior_stdout
            st.rerun()

    if st.session_state[_SS_ERR]:
        st.error(st.session_state[_SS_ERR])
    if st.session_state[_SS_PLAN]:
        st.markdown(
            '<p id="streamlit-action-plan-anchor" style="margin:0;padding:0;"></p>',
            unsafe_allow_html=True,
        )
        st.success("✅ Workflow completed!")
        st.subheader("📄 Action Plan")
        st.markdown(st.session_state[_SS_PLAN])
        if st.session_state.get(_SS_SCROLL):
            _scroll_action_plan_into_view()
            st.session_state[_SS_SCROLL] = False
