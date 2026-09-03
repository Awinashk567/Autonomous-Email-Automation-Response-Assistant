# 🚀 Autonomous AOL Mail AI Assistant (Cloud-Ready)

An automated AI-powered email assistant built using **Python**, **Playwright**, **Flask**, and **Groq AI (Llama 3.1)**. This bot monitors your AOL Mail inbox 24/7, detects unread messages, filters out promotional ads, generates a natural human-like response contextually, and replies automatically.

---

## ✨ Features

- **🧠 Advanced AI Integration:** Powered by Groq (`llama-3.1-8b-instant`) for fast, natural, and human-like replies.
- **🌐 24/7 Cloud Deployment:** Includes a dummy Flask web server designed to keep the app alive on cloud hosting platforms like Render.
- **👻 Smart Popup Killer:** Automatically handles and dismisses unwanted AOL popups or banners.
- **🛡️ Session Persistence:** Saves cookies and session state (`aol_session.json`) to avoid repeated logins.
- **🚫 Ad-Blocker Logic:** Distinguishes between genuine unread emails and promotional ads.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Playwright** (Browser Automation)
- **Flask** (Dummy Web Server for cloud keep-alive)
- **Groq API / OpenAI Client** (AI Text Generation)
- **Python-Dotenv** (Environment Configuration)

---

## ⚙️ Installation & Local Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name
