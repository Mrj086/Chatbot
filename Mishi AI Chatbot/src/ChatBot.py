import streamlit as st
from google import genai

st.set_page_config(
    page_title="Mishi AI",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0f0f13; color: #e8e8f0; }
#MainMenu, footer, header {visibility: hidden;}
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 720px; }

.mishi-header { text-align: center; padding: 2rem 0 1.5rem; }
.mishi-header h1 { font-size: 2rem; font-weight: 600; color: #a78bfa; letter-spacing: -0.5px; margin: 0; }
.mishi-header p { font-size: 0.9rem; color: #6b6b80; margin: 0.4rem 0 0; }

.msg-user { display: flex; justify-content: flex-end; margin: 0.75rem 0; }
.msg-ai   { display: flex; justify-content: flex-start;  margin: 0.75rem 0; }
.bubble-user { background: #6d28d9; color: #f5f3ff; padding: 0.75rem 1.1rem; border-radius: 18px 18px 4px 18px; max-width: 80%; font-size: 0.92rem; line-height: 1.6; }
.bubble-ai   { background: #1c1c2e; color: #e2e2f0; padding: 0.75rem 1.1rem; border-radius: 18px 18px 18px 4px; max-width: 80%; font-size: 0.92rem; line-height: 1.6; border: 1px solid #2a2a40; }
.avatar { width: 28px; height: 28px; border-radius: 50%; background: #6d28d9; color: white; font-size: 0.75rem; display: flex; align-items: center; justify-content: center; margin-right: 8px; flex-shrink: 0; font-weight: 600; margin-top: 2px; }

section[data-testid="stSidebar"] { background: #0a0a10; border-right: 1px solid #1e1e2e; }
section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

.stTextInput > div > div > input {
    background: #1c1c2e !important; border: 1px solid #2a2a40 !important;
    color: #e8e8f0 !important; border-radius: 12px !important;
    padding: 0.6rem 1rem !important; font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus { border-color: #6d28d9 !important; box-shadow: 0 0 0 2px rgba(109,40,217,0.2) !important; }

.stButton > button {
    background: #6d28d9 !important; color: white !important; border: none !important;
    border-radius: 12px !important; padding: 0.55rem 1.4rem !important;
    font-family: 'Inter', sans-serif !important; font-weight: 500 !important; font-size: 0.9rem !important;
}
.stButton > button:hover { background: #5b21b6 !important; }

.empty-state { text-align: center; padding: 3rem 1rem; color: #4a4a60; }
.empty-state .icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
.empty-state p { font-size: 0.9rem; line-height: 1.6; }
hr { border-color: #1e1e2e; }
</style>
""", unsafe_allow_html=True)


# ── Session state — must be before anything else ──────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = None
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "input_value" not in st.session_state:
    st.session_state.input_value = ""
if "pending_message" not in st.session_state:
    st.session_state.pending_message = ""
if "client" not in st.session_state:
    st.session_state.client = None


# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 Mishi AI")
    st.markdown("<p style='color:#6b6b80;font-size:0.82rem;'>Powered by Google Gemini</p>", unsafe_allow_html=True)
    st.divider()

    typed_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your API key here",
        help="Get a free key at aistudio.google.com",
        key="key_input"
    )

    # Save key permanently in session state whenever user types it
    if typed_key:
        st.session_state.api_key = typed_key
        st.markdown("<p style='color:#4ade80;font-size:0.78rem;margin-top:4px;'>✅ API key saved</p>", unsafe_allow_html=True)
    elif st.session_state.api_key:
        st.markdown("<p style='color:#4ade80;font-size:0.78rem;margin-top:4px;'>✅ API key saved</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#f87171;font-size:0.78rem;margin-top:4px;'>⚠️ Enter your API key to start</p>", unsafe_allow_html=True)

    st.divider()

    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.session_state.chat = None
        st.session_state.client = None
        st.rerun()

    st.markdown("""
    <div style='margin-top:2rem;'>
        <p style='color:#4a4a60;font-size:0.78rem;line-height:1.6;'>
            Built by <strong style='color:#6d28d9;'>Miraj</strong><br>
            CS Student · Bangladesh<br><br>
            <a href='https://github.com/Mrj086/MishiAIchatbot'
               style='color:#6d28d9;text-decoration:none;'>GitHub ↗</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────
st.markdown("""
<div class='mishi-header'>
    <h1>✨ Mishi AI</h1>
    <p>Your intelligent conversation partner</p>
</div>
""", unsafe_allow_html=True)


# ── Chat history ──────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class='empty-state'>
        <div class='icon'>💬</div>
        <p>Ask me anything — coding, ideas,<br>explanations, or just a chat.</p>
    </div>
    """, unsafe_allow_html=True)

    suggestions = [
        "Explain machine learning simply",
        "Help me write a Python function",
        "What is Data Science?",
        "Give me study tips for exams",
    ]
    cols = st.columns(2)
    for i, s in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(s, key=f"sug_{i}", use_container_width=True):
                st.session_state.pending_message = s
                st.rerun()
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class='msg-user'>
                <div class='bubble-user'>{msg['content']}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='msg-ai'>
                <div class='avatar'>M</div>
                <div class='bubble-ai'>{msg['content']}</div>
            </div>""", unsafe_allow_html=True)


# ── Input — uses a form so Enter key works ────────────────
st.divider()
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "message",
            label_visibility="collapsed",
            placeholder="Message Mishi... (press Enter to send)",
            value=st.session_state.input_value,
            key="chat_input"
        )
    with col2:
        submitted = st.form_submit_button("Send", use_container_width=True)



# ── Handle suggestion chip clicks ─────────────────────────
def send_message(text):
    if not st.session_state.api_key:
        st.error("⚠️ Please paste your Gemini API key in the sidebar first.")
        return
    if st.session_state.client is None:
        try:
            st.session_state.client = genai.Client(api_key=st.session_state.api_key)
        except Exception as e:
            st.error(f"Could not connect to Gemini: {e}")
            return
    if st.session_state.chat is None:
        try:
            st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")
        except Exception as e:
            st.error(f"Could not create chat session: {e}")
            return
    st.session_state.messages.append({"role": "user", "content": text})
    with st.spinner("Mishi is thinking..."):
        try:
            response = st.session_state.chat.send_message(text)
            ai_reply = response.text
        except Exception as e:
            ai_reply = f"Sorry, something went wrong: {e}"
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

if st.session_state.pending_message:
    msg = st.session_state.pending_message
    st.session_state.pending_message = ""
    send_message(msg)
    st.rerun()

# ── Response logic ────────────────────────────────────────
if submitted and user_input.strip():
    send_message(user_input.strip())
    st.rerun()