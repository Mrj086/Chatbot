import streamlit as st
from google import genai
import time

st.set_page_config(
    page_title="Mishi AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

*, html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0f0f13 !important;
    color: #e8e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stMain"] { background: #0f0f13 !important; }
[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
.stDeployButton { display: none !important; }
#MainMenu, footer { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0a0a10 !important;
    border-right: 1px solid #1e1e2e !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* ── Buttons ── */
.stButton > button {
    background: rgba(109,40,217,0.1) !important;
    border: 1px solid #2a2a40 !important;
    color: #e8e8f0 !important;
    border-radius: 12px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all .2s !important;
    width: 100% !important;
    text-align: left !important;
    padding: 0.55rem 1rem !important;
}
.stButton > button:hover {
    background: rgba(109,40,217,0.22) !important;
    border-color: #6d28d9 !important;
}

/* ── Chat input — dark background, purple border ── */
[data-testid="stChatInput"] {
    background: #13131f !important;
    border: 1.5px solid #6d28d9 !important;
    border-radius: 24px !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #e8e8f0 !important;
    font-size: 15px !important;
    border: none !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(109,40,217,0.2) !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #6d28d9, #a78bfa) !important;
    border-radius: 50% !important;
    border: none !important;
}
[data-testid="stChatInput"] button svg { fill: white !important; }

/* ── Chat messages — remove default bg ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 4px 0 !important;
    gap: 12px !important;
}

/* ── USER messages → RIGHT side ── */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse !important;
    text-align: right !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) > div:nth-child(2) {
    align-items: flex-end !important;
    display: flex !important;
    flex-direction: column !important;
}
/* Fallback using data-testid stChatMessageContent */
div:has(> [data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse !important;
}

/* ── Thinking animation ── */
@keyframes thinking {
    0%,80%,100% { transform: scale(0.6); opacity: 0.4; }
    40%          { transform: scale(1.0); opacity: 1.0; }
}
@keyframes thinkingSlideIn {
    0%   { opacity: 0; transform: translateX(-16px) translateY(4px); }
    100% { opacity: 1; transform: translateX(0) translateY(0); }
}
@keyframes thinkingPulse {
    0%,100% { box-shadow: 0 0 0px rgba(167,139,250,0); }
    50%      { box-shadow: 0 0 14px rgba(167,139,250,0.45); }
}
@keyframes thinkingTextBlink {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.4; }
}
.thinking-wrap {
    animation: thinkingSlideIn 0.4s cubic-bezier(.22,.68,0,1.2) both;
}
.thinking-bubble {
    animation: thinkingPulse 2s ease-in-out infinite;
}
.thinking-text {
    animation: thinkingTextBlink 1.6s ease-in-out infinite;
}
.thinking-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #a78bfa;
    margin: 0 2px;
    animation: thinking 1.2s infinite ease-in-out;
}
.thinking-dot:nth-child(2) { animation-delay: 0.2s; }
.thinking-dot:nth-child(3) { animation-delay: 0.4s; }
.thinking-label {
    font-size: 12px; color: #6b6b80;
    display: flex; align-items: center; gap: 8px;
    padding: 8px 0 4px;
}

/* ── Streaming text animation ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to   { opacity: 1; transform: translateY(0); }
}
.ai-response { animation: fadeIn 0.3s ease; }

/* ── AI message bubble animation ── */
@keyframes msgSlideIn {
    0%   { opacity: 0; transform: translateX(-18px) translateY(6px); }
    60%  { opacity: 1; transform: translateX(4px) translateY(0); }
    100% { opacity: 1; transform: translateX(0) translateY(0); }
}
@keyframes bubblePop {
    0%   { transform: scale(0.92); opacity: 0; }
    60%  { transform: scale(1.03); opacity: 1; }
    100% { transform: scale(1);    opacity: 1; }
}
.ai-msg-wrap   { animation: msgSlideIn 0.45s cubic-bezier(.22,.68,0,1.2) both; }
.ai-msg-bubble { animation: bubblePop  0.4s  cubic-bezier(.22,.68,0,1.2) 0.1s both; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0f0f13; }
::-webkit-scrollbar-thumb { background: #2a2a40; border-radius: 3px; }

/* ── Code blocks ── */
.stMarkdown pre { background: #1c1c2e !important; border: 1px solid #2a2a40 !important; border-radius: 10px !important; }
code { color: #a78bfa !important; }
hr { border-color: #1e1e2e !important; }

/* ── Mobile sidebar toggle button ── */
#sidebar-toggle-btn {
    display: none;
    position: fixed;
    top: 14px;
    right: 14px;
    left: auto;
    z-index: 999999;
    background: linear-gradient(135deg,#6d28d9,#a78bfa);
    border: none;
    border-radius: 10px;
    width: 40px;
    height: 40px;
    cursor: pointer;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    box-shadow: 0 0 14px rgba(109,40,217,0.5);
    transition: all 0.2s;
}
#sidebar-toggle-btn:hover {
    transform: scale(1.08);
    box-shadow: 0 0 20px rgba(109,40,217,0.7);
}
@media (max-width: 768px) {
    #sidebar-toggle-btn { display: flex; }
}
</style>

<button id="sidebar-toggle-btn" title="Open Menu">☰</button>

<script>
(function() {
    function tryClick() {
        // Streamlit's native collapse/expand button selectors
        var selectors = [
            '[data-testid="collapsedControl"]',
            '[data-testid="baseButton-headerNoPadding"]',
            'button[aria-label="open sidebar"]',
            'button[aria-label="close sidebar"]',
            'section[data-testid="stSidebar"] + div button',
            'button[kind="header"]'
        ];
        var doc = window.parent ? window.parent.document : document;
        for (var i = 0; i < selectors.length; i++) {
            var btn = doc.querySelector(selectors[i]);
            if (btn) { btn.click(); return true; }
        }
        // Fallback: directly toggle sidebar style
        var sidebar = doc.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            var curr = sidebar.style.marginLeft;
            sidebar.style.marginLeft = (curr === '0px' || curr === '') ? '-21rem' : '0px';
            sidebar.style.transition = 'margin-left 0.3s ease';
            return true;
        }
        return false;
    }

    document.getElementById('sidebar-toggle-btn').addEventListener('click', function() {
        if (!tryClick()) {
            setTimeout(tryClick, 300);
        }
    });
})();
</script>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "client" not in st.session_state:
    st.session_state.client = None
if "chat" not in st.session_state:
    st.session_state.chat = None
if "pending" not in st.session_state:
    st.session_state.pending = ""
if "recent_chats" not in st.session_state:
    st.session_state.recent_chats = []


# ── Init Gemini once ──────────────────────────────────────
if st.session_state.client is None:
    try:
        st.session_state.client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.error(f"Failed to connect to Gemini: {e}")
        st.stop()

if st.session_state.chat is None:
    try:
        st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")
    except Exception as e:
        st.error(f"Failed to start chat: {e}")
        st.stop()


# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:20px 16px 16px;">
        <div style="width:34px;height:34px;border-radius:10px;
                    background:linear-gradient(135deg,#6d28d9,#a78bfa);
                    display:flex;align-items:center;justify-content:center;font-size:16px;
                    box-shadow:0 0 16px rgba(109,40,217,.4);">✨</div>
        <span style="font-family:'Space Grotesk',sans-serif;font-size:17px;font-weight:700;
                     color:#a78bfa;">Mishi AI</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✏️  New Chat", key="new_chat"):
        st.session_state.messages = []
        st.session_state.chat = None
        try:
            st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")
        except Exception as e:
            st.error(f"Could not start new chat: {e}")
        st.rerun()

    st.markdown("""
    <div style="font-size:11px;font-weight:600;text-transform:uppercase;
                letter-spacing:.08em;color:#555870;padding:14px 14px 6px;">Recent</div>
    """, unsafe_allow_html=True)

    if st.session_state.recent_chats:
        for label in reversed(st.session_state.recent_chats[-8:]):
            short = (label[:32] + "…") if len(label) > 32 else label
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:7px 12px;
                        border-radius:8px;font-size:13px;color:#6b6b80;">
                <span style="font-size:11px;flex-shrink:0;">💬</span>
                <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{short}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="font-size:12px;color:#3a3d50;padding:6px 14px;font-style:italic;">
            Your chats will appear here
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:14px 0'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:10px 12px;
                background:#13131f;border:1px solid #1e1e2e;border-radius:12px;margin:0 8px 8px;">
        <div style="width:30px;height:30px;border-radius:50%;
                    background:linear-gradient(135deg,#6d28d9,#a78bfa);
                    display:flex;align-items:center;justify-content:center;
                    font-size:13px;font-weight:700;color:white;flex-shrink:0;">M</div>
        <div>
            <div style="font-size:13px;font-weight:500;color:#e8e8f0;">Miraj</div>
            <div style="font-size:11px;color:#555870;">CSE Student · Bangladesh</div>
        </div>
    </div>
    <div style="font-size:11px;color:#3a3d50;padding:4px 14px 8px;line-height:1.9;">
        🔗 <a href="https://github.com/Mrj086/MishiAIchatbot" target="_blank"
               style="color:#3b82f6;text-decoration:none;">GitHub</a> ·
        <a href="https://www.linkedin.com/in/md-miraj-ul-islam-77b30b26a/" target="_blank"
           style="color:#3b82f6;text-decoration:none;">LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)


# ── Top bar ───────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:12px 8px;border-bottom:1px solid #1e1e2e;margin-bottom:4px;">
    <div style="display:flex;align-items:center;gap:10px;">
        <span style="font-family:'Space Grotesk',sans-serif;font-size:17px;font-weight:700;color:#e8e8f0;">Mishi</span>
        <span style="font-size:11px;color:#555870;background:#13131f;border:1px solid #1e1e2e;
                     border-radius:20px;padding:2px 10px;">gemini-2.5-flash</span>
    </div>
    <span style="font-size:11px;color:#3a3d50;">Intelligent AI Companion</span>
</div>
""", unsafe_allow_html=True)


# ── Welcome screen ────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center;padding:52px 20px 24px;">
        <div style="display:inline-flex;align-items:center;gap:12px;margin-bottom:14px;">
            <div style="width:52px;height:52px;border-radius:16px;
                        background:linear-gradient(135deg,#6d28d9,#a78bfa);
                        display:flex;align-items:center;justify-content:center;
                        font-size:26px;flex-shrink:0;
                        box-shadow:0 0 28px rgba(109,40,217,.5);">✨</div>
            <span style="font-family:'Space Grotesk',sans-serif;font-size:28px;font-weight:700;
                      color:#a78bfa !important;-webkit-text-fill-color:#a78bfa !important;
                      letter-spacing:0.3px;">Mishi AI</span>
        </div>
        <h1 style="font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;
                   color:#e8e8f0;margin:0 0 10px;">Hi! there, I am Mishi</h1>
        <p style="font-size:15px;color:#6b6b80;margin:0 auto 6px;max-width:440px;">
            Your Intelligent conversation partner.
        </p>
        <p style="font-size:13px;color:#3a3d50;margin:0 auto 32px;max-width:440px;">
            What do you want to know or learn today? I am here to help.
        </p>
    </div>
    """, unsafe_allow_html=True)

    suggestions = [
        ("📊", "What is Data Science?",       "What is Data Science and why is it important in today's world?"),
        ("✍️", "Write me a short poem",       "Write me a beautiful short poem about the stars and the night sky"),
        ("🎵", "Make a song for me",          "Write a short uplifting song with a chorus and two verses"),
        ("📚", "Daily routine for a student", "Make a daily routine for an ideal university student who wants to excel"),
    ]
    c1, c2 = st.columns(2)
    for i, (icon, title, prompt) in enumerate(suggestions):
        with (c1 if i % 2 == 0 else c2):
            if st.button(f"{icon}  {title}", key=f"sug_{i}", use_container_width=True):
                st.session_state.pending = prompt
                st.rerun()

else:
    # ── Render chat history ───────────────────────────────
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.markdown(f"""
            <div class="ai-msg-wrap" style="display:flex;align-items:flex-start;gap:10px;margin:10px 0;justify-content:flex-start;">
                <div style="width:32px;height:32px;border-radius:50%;flex-shrink:0;
                            background:linear-gradient(135deg,#6d28d9,#a78bfa);
                            display:flex;align-items:center;justify-content:center;font-size:14px;">✨</div>
                <div class="ai-msg-bubble" style="background:#1c1c2e;border:1px solid #2a2a40;border-radius:4px 18px 18px 18px;
                            padding:12px 16px;max-width:75%;font-size:14px;line-height:1.7;color:#e8e8f0;">
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:10px;margin:10px 0;justify-content:flex-end;">
                <div style="background:#6d28d9;border-radius:18px 4px 18px 18px;
                            padding:12px 16px;max-width:75%;font-size:14px;line-height:1.7;color:#f5f3ff;">
                    {msg['content']}
                </div>
                <div style="width:32px;height:32px;border-radius:50%;flex-shrink:0;
                            background:linear-gradient(135deg,#4f46e5,#7c3aed);
                            display:flex;align-items:center;justify-content:center;
                            font-size:12px;font-weight:700;color:white;">You</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;font-size:11px;color:#2a2a40;padding:8px 0 2px;">
        Mishi AI can make mistakes. Please verify important information.
    </div>
    """, unsafe_allow_html=True)


# ── Handle pending suggestion ─────────────────────────────
if st.session_state.pending:
    prompt = st.session_state.pending
    st.session_state.pending = ""

    st.session_state.messages.append({"role": "user", "content": prompt})
    # Show user message immediately RIGHT
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;gap:10px;margin:10px 0;justify-content:flex-end;">
        <div style="background:#6d28d9;border-radius:18px 4px 18px 18px;
                    padding:12px 16px;max-width:75%;font-size:14px;line-height:1.7;color:#f5f3ff;">
            {prompt}
        </div>
        <div style="width:32px;height:32px;border-radius:50%;flex-shrink:0;
                    background:linear-gradient(135deg,#4f46e5,#7c3aed);
                    display:flex;align-items:center;justify-content:center;
                    font-size:12px;font-weight:700;color:white;">You</div>
    </div>
    """, unsafe_allow_html=True)

    # Track recent
    short = prompt[:40]
    if not st.session_state.recent_chats or st.session_state.recent_chats[-1] != short:
        st.session_state.recent_chats.append(short)

    thinking_ph = st.empty()
    thinking_ph.markdown("""
    <div class="thinking-wrap" style="display:flex;align-items:center;gap:10px;margin:10px 0;justify-content:flex-start;">
        <div style="width:32px;height:32px;border-radius:50%;flex-shrink:0;
                    background:linear-gradient(135deg,#6d28d9,#a78bfa);
                    display:flex;align-items:center;justify-content:center;font-size:14px;">✨</div>
        <div class="thinking-bubble" style="background:#1c1c2e;border:1px solid #2a2a40;border-radius:4px 18px 18px 18px;
                    padding:12px 16px;font-size:14px;color:#6b6b80;">
            <span class="thinking-text">Mishi is thinking</span>
            <span class="thinking-dot"></span>
            <span class="thinking-dot"></span>
            <span class="thinking-dot"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    try:
        response = st.session_state.chat.send_message(prompt)
        reply = response.text
    except Exception as e:
        reply = f"Something went wrong: {e}"
    thinking_ph.empty()
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()


# ── Chat input ────────────────────────────────────────────
user_input = st.chat_input("Ask Mishi anything…")

if user_input:
    text = user_input.strip()

    st.session_state.messages.append({"role": "user", "content": text})
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;gap:10px;margin:10px 0;justify-content:flex-end;">
        <div style="background:#6d28d9;border-radius:18px 4px 18px 18px;
                    padding:12px 16px;max-width:75%;font-size:14px;line-height:1.7;color:#f5f3ff;">
            {text}
        </div>
        <div style="width:32px;height:32px;border-radius:50%;flex-shrink:0;
                    background:linear-gradient(135deg,#4f46e5,#7c3aed);
                    display:flex;align-items:center;justify-content:center;
                    font-size:12px;font-weight:700;color:white;">You</div>
    </div>
    """, unsafe_allow_html=True)

    # Track recent
    short = text[:40]
    if not st.session_state.recent_chats or st.session_state.recent_chats[-1] != short:
        st.session_state.recent_chats.append(short)

    thinking_box = st.empty()
    thinking_box.markdown("""
    <div class="thinking-wrap" style="display:flex;align-items:center;gap:10px;margin:10px 0;justify-content:flex-start;">
        <div style="width:32px;height:32px;border-radius:50%;flex-shrink:0;
                    background:linear-gradient(135deg,#6d28d9,#a78bfa);
                    display:flex;align-items:center;justify-content:center;font-size:14px;">✨</div>
        <div class="thinking-bubble" style="background:#1c1c2e;border:1px solid #2a2a40;border-radius:4px 18px 18px 18px;
                    padding:12px 16px;font-size:14px;color:#6b6b80;">
            <span class="thinking-text">Mishi is thinking</span>
            <span class="thinking-dot"></span>
            <span class="thinking-dot"></span>
            <span class="thinking-dot"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    try:
        response = st.session_state.chat.send_message(text)
        reply = response.text
    except Exception as e:
        reply = f"Something went wrong: {e}"
    thinking_box.empty()
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
