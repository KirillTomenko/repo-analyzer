# 🤖 AI GitHub Repo Analyzer

> **Instant AI-powered code review for any public GitHub repository — right in your terminal.**

Paste a GitHub URL → get a full structured analysis powered by GPT-4o in seconds.

---

## ✨ What it does

- 📦 Fetches repo metadata, file structure, README and recent commits via **GitHub API**
- 🧠 Sends it all to **GPT-4o** for deep analysis
- 📊 Outputs a beautiful **scored report** with strengths, issues and priority actions
- 🐳 Runs anywhere via **Docker** — no Python setup needed

---

## 📸 Example Output

```
╭─────────────────────────────────────────────────────╮
│ 🔍 KirillTomenko/business-ideas-generator-cloud     │
│  ☁️ AI-агент для генерации бизнес-идей              │
│  ⭐ Stars: 1  🍴 Forks: 0  🐛 Issues: 0            │
│  📝 License: MIT  🔄 Updated: 2026-02-19            │
╰─────────────────────────────────────────────────────╯

╭──────────────── 🤖 AI Analysis Report ─────────────────╮
│                                                         │
│ ## 🎯 Project Overview                                  │
│ A FastAPI-based AI agent that generates business        │
│ ideas using GPT-4o with market analysis...              │
│                                                         │
│ ## ✅ Strengths                                         │
│ - Clean Docker integration with ENV management          │
│ - Good use of FastAPI for async endpoints               │
│ ...                                                     │
│                                                         │
│ ## 📊 Overall Score                                     │
│ - Code Quality:    8/10                                 │
│ - Documentation:   7/10                                 │
│ - Security:        9/10                                 │
│ - Architecture:    8/10                                 │
│ - **Overall: 8/10**                                     │
╰─────────────────────────────────────────────────────────╯
```

---

## 🚀 Quick Start

### Option 1: Docker (recommended)

```bash
# Build
git clone https://github.com/KirillTomenko/repo-analyzer.git
cd repo-analyzer
docker build -t repo-analyzer .

# Run
docker run -e OPENAI_API_KEY=your_key repo-analyzer https://github.com/user/repo
```

### Option 2: Python

```bash
git clone https://github.com/KirillTomenko/repo-analyzer.git
cd repo-analyzer
pip install -r requirements.txt

export OPENAI_API_KEY=your_key
python main.py https://github.com/user/repo
```

---

## 📋 Report Structure

| Section | Description |
|---|---|
| 🎯 Project Overview | What the project does and its purpose |
| ✅ Strengths | What's done well |
| ⚠️ Areas for Improvement | Specific, actionable issues |
| 🔒 Security & Best Practices | Secrets, dependencies, vulnerabilities |
| 📁 Code Structure | Architecture and maintainability |
| 📊 Scores | Code Quality, Docs, Security, Architecture (1-10) |
| 🚀 Priority Actions | Top 3 things to do next |

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| GPT-4o (OpenAI) | AI analysis engine |
| GitHub REST API | Repository data fetching |
| Rich | Beautiful terminal output |
| Docker | Containerization |

---

## 🔒 Security Note

Your `OPENAI_API_KEY` is passed as an environment variable at runtime — it is **never** stored in the image or code.

```bash
# ✅ Safe — key only exists for this run
docker run -e OPENAI_API_KEY=sk-... repo-analyzer https://github.com/...
```

---

## 🗂 Project Structure

```
repo-analyzer/
├── main.py           # CLI entry point & argument parsing
├── analyzer.py       # GitHub API + GPT-4o analysis logic
├── Dockerfile        # Container definition
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variable template
└── .gitignore
```

---

## 👤 Author

**Kirill Tomenko** · [GitHub](https://github.com/KirillTomenko) · [Telegram](https://t.me/Kirill_BT)

> Part of my AI tools portfolio — building practical AI agents with Python & Docker.

---

## 📄 License

MIT — free to use, modify and distribute.
