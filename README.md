# ✨ Mishi AI — Conversational AI Chatbot

A fully functional AI chatbot web app built with Python and Streamlit, powered by **Google Gemini 2.5 Flash**. Features a clean dark UI, persistent conversation memory, and one-click suggestion prompts.

> Built by [MD. Miraj-Ul-Islam](https://www.linkedin.com/in/md-miraj-ul-islam-77b30b26a/) — CS Student | AI & Data Science Enthusiast | Bangladesh 🇧🇩

---

## 🖥️ Preview

![Mishi AI Screenshot](screenshot.png)

---

## ✨ Features

- 💬 Multi-turn conversation with full context memory
- ⚡ Powered by Google Gemini 2.5 Flash
- 🎨 Dark purple UI built with Streamlit
- 💡 One-click suggestion chips to get started instantly
- ⌨️ Send messages with Enter key or Send button
- 🔒 Secure API key input — never hardcoded
- 🗑️ Clear chat button to start fresh anytime
- 📱 Responsive layout

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.8+ |
| Framework | Streamlit |
| AI Model | Google Gemini 2.5 Flash |
| Library | `google-genai` |
| Interface | Web browser |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Mrj086/MishiAIchatbot.git
cd MishiAIchatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a free Gemini API key

Go to [aistudio.google.com](https://aistudio.google.com), sign in with your Google account, and click **Get API Key → Create API key**. It is completely free.

### 4. Run the app

```bash
streamlit run ChatBot.py
```

Your browser will open automatically at `http://localhost:8501`

### 5. Start chatting

Paste your Gemini API key in the sidebar — you will see a green ✅ confirmation. Then type your message or click a suggestion chip and chat away!

---

## 📁 Project Structure

```
MishiAI/
├── ChatBot.py          # Main app — UI + Gemini API logic
├── requirements.txt    # Python dependencies
├── .gitignore          # Files excluded from Git
├── LICENSE             # MIT License
└── README.md           # You are here
```

---

## 🧠 What I Learned

- Building a full-stack AI web app with Streamlit
- Integrating Google Gemini API with multi-turn conversation memory
- Managing Streamlit session state across reruns
- Handling API connections persistently in a stateless framework
- Designing a custom dark-themed UI with CSS inside Streamlit

---

## 🔮 Roadmap

- [ ] Deploy live on Streamlit Cloud
- [ ] Add Bengali language support 🇧🇩
- [ ] Let users switch between Gemini models
- [ ] Add chat export (download conversation as .txt)
- [ ] Voice input support

---

## 👤 Author

**MD. Miraj-Ul-Islam**
CS Student | AI & Data Science Enthusiast | Bangladesh

🔗 [LinkedIn](https://www.linkedin.com/in/md-miraj-ul-islam-77b30b26a/) · [GitHub](https://github.com/Mrj086)

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
