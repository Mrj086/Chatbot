# 🤖 Mishi AI — Terminal Chatbot powered by Google Gemini

Mishi AI is a command-line conversational chatbot built with Python and powered by **Google Gemini 2.5 Flash**. It lets you have a real-time AI conversation directly from your terminal.

> Built by MD. Miraj-Ul-Islam — CS Student | AI & Data Science enthusiast | Bangladesh

---

## 💬 Demo

```
🤖 Mishi AI Chatbot
Type 'exit' to quit.

You: What is machine learning?

Mishi: Machine learning is a branch of AI where systems learn
from data to improve their performance without being explicitly
programmed...
```

---

## ✨ Features

- 🔁 Continuous conversation loop — chat until you type `exit`
- ⚡ Powered by Gemini 2.5 Flash — fast and capable
- 🛡️ Basic error handling for API failures
- 🪶 Lightweight — just one Python file

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.8+ |
| AI Model | Google Gemini 2.5 Flash |
| Library | `google-genai` |
| Interface | Command Line (Terminal) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- A free [Google Gemini API key](https://makersuite.google.com/app/apikey)

### Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/Mrj086/MishiAIchatbot.git
cd MishiAIchatbot

# 2. Install dependency
pip install -q -U google-genai

# 3. Run the chatbot
python ChatBot.py

# 4. Enter your Gemini API key when prompted
```

---

## 📁 Project Structure

```
MishiAI/
├── ChatBot.py          # Main chatbot logic + Gemini API integration
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License
└── README.md
```

---

## 🧠 What I Learned

- How to integrate Google Gemini API into a Python project
- How to build a clean conversational loop with error handling
- How to work with the `google-genai` SDK

---

## 🔮 Roadmap (planned upgrades)

- [ ] Add web interface using Streamlit
- [ ] Maintain multi-turn conversation history (context memory)
- [ ] Add Bengali language support 🇧🇩
- [ ] Secure API key via `.env` file instead of manual input
- [ ] Let users choose between Gemini models

---

## 👤 Author

**MD. Miraj-Ul-Islam**
CS Student | AI & Data Science Enthusiast | Bangladesh
🔗 [LinkedIn](https://www.linkedin.com/in/md-miraj-ul-islam-77b30b26a/) · [GitHub](https://github.com/Mrj086)

---

## 📄 License

MIT License — feel free to use and build on this project.
