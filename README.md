<div align="center">

# 🧠 GenAI Diagrams as Code

### _Transform natural language & source code into professional UML diagrams — powered by Google Gemini AI_

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![PlantUML](https://img.shields.io/badge/PlantUML-Diagrams-green?style=for-the-badge)](https://plantuml.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br>

<img src="https://img.shields.io/badge/status-Active-brightgreen?style=flat-square" alt="Status">
<img src="https://img.shields.io/badge/PRs-Welcome-blue?style=flat-square" alt="PRs Welcome">

---

**Describe** your system in plain English → **AI generates** PlantUML code → **Instant visual** diagram

</div>

<br>

## 📸 Overview

A full-stack Django web application that uses **Google's Gemini 2.0 Flash** AI model to convert:

- 📝 **Natural language descriptions** → UML Diagrams  
- 💻 **Source code files** (.py, .java, .js, .txt) → UML Diagrams  
- 🖼️ **Uploaded images** of diagrams → PlantUML code representation  

The generated PlantUML code is rendered into visual diagrams in real-time using the PlantUML public server.

<br>

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Diagram Generation** | Describe what you want in plain English and get a diagram |
| 📂 **File Upload Support** | Upload `.py`, `.java`, `.js`, `.txt`, or image files |
| 🖼️ **Image-to-Code** | Upload an image of a diagram and get PlantUML code back |
| 📋 **One-Click Copy** | Copy generated PlantUML code to clipboard instantly |
| 👤 **User Authentication** | Register, login, and manage your session |
| 🛡️ **Admin Dashboard** | Activate, deactivate, or delete user accounts |
| 🌙 **Dark Cyber UI** | Futuristic glassmorphism interface with neon accents |
| 📱 **Responsive Design** | Works seamlessly on desktop & mobile devices |

<br>

## 🏗️ Tech Stack

```
Frontend    →  HTML5 · CSS3 (Custom Properties) · Vanilla JS · Font Awesome 6
Backend     →  Django 6.0 · Python 3.12
AI Engine   →  Google Generative AI (Gemini 2.0 Flash)
Diagrams    →  PlantUML (via public rendering server)
Database    →  SQLite3
Fonts       →  Outfit · JetBrains Mono (Google Fonts)
```

<br>

## 📁 Project Structure

```
📦 GenAI-Diagrams-as-Code/
├── 📄 manage.py                    # Django management script
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment variable template
├── 📄 .gitignore                   # Git ignore rules
│
├── 📂 Generative_AI_.../           # Django project settings
│   ├── settings.py                 # Configuration (DB, API keys, static files)
│   ├── urls.py                     # All URL routes
│   ├── views.py                    # Main views (index, login pages)
│   ├── wsgi.py / asgi.py           # Server entry points
│
├── 📂 users/                       # User app
│   ├── models.py                   # UserRegistrationModel
│   ├── forms.py                    # Registration form
│   ├── views.py                    # User auth + AI diagram generation logic
│
├── 📂 admins/                      # Admin app
│   ├── views.py                    # Admin login, user management
│
├── 📂 templates/                   # HTML templates
│   ├── base.html                   # Master layout (nav, footer, CSS)
│   ├── index.html                  # Landing page
│   ├── UserLogin.html              # User login form
│   ├── UserRegistration.html       # Registration form
│   ├── AdminLogin.html             # Admin login form
│   ├── users/                      # User-specific pages
│   │   ├── UserHome.html           # User dashboard
│   │   └── generate.html           # AI diagram generator (main feature)
│   └── admins/                     # Admin-specific pages
│       ├── AdminHome.html          # Admin dashboard
│       └── viewregister.html       # User management table
│
└── 📂 static/                      # Static assets
    └── css/
        └── main.css                # Global design system
```

<br>

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+** — [Download here](https://www.python.org/downloads/)
- **Git** — [Download here](https://git-scm.com/downloads)
- **Google API Key** — [Get one free at Google AI Studio](https://aistudio.google.com/app/apikey)

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/RasheedAli-Shaik/GenAI-Diagrams-as-Code.git
cd GenAI-Diagrams-as-Code
```

### 2️⃣ Create & Activate Virtual Environment

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env          # Linux/macOS
copy .env.example .env        # Windows
```

Then open `.env` and paste your Google API key:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

> 💡 **Get your key:** Visit [Google AI Studio](https://aistudio.google.com/app/apikey) → Create API Key → Copy it.

### 5️⃣ Run Database Migrations

```bash
python manage.py migrate
```

### 6️⃣ Start the Development Server

```bash
python manage.py runserver
```

### 7️⃣ Open in Browser

```
🌐  http://127.0.0.1:8000
```

<br>

## 👤 Default Credentials

| Role | Username | Password |
|:---:|:---:|:---:|
| 🛡️ Admin | `admin` | `admin` |
| 👤 User | _Register a new account_ | — |

> New users must be **activated** by the admin before they can log in.

<br>

## 🎯 Usage Guide

1. **Register** a new user account at `/UserRegister/`
2. **Admin activates** your account — login as `admin` / `admin` at `/AdminLogin/`
3. **Login** with your credentials at `/UserLogin/`
4. **Navigate** to the **Generate** page
5. **Enter a prompt** like:
   > _"Create a class diagram for a library management system with Book, Member, and Librarian classes"_
6. **Or upload** a source code file (`.py`, `.java`, `.js`, `.txt`)
7. Click **Generate Diagram** and watch the magic happen ✨
8. **Copy** the PlantUML code or view the rendered diagram

<br>

## 🧪 Example Prompts

```
📌  "Sequence diagram for user authentication flow with Frontend, API Gateway, Auth Service, and Database"

📌  "Class diagram for an e-commerce system with Product, Cart, Order, Payment, and User classes"

📌  "Activity diagram for a CI/CD pipeline from code commit to production deployment"

📌  "Component diagram showing a microservices architecture for a food delivery app"
```

<br>

## ⚙️ Configuration Reference

| Variable | Location | Purpose |
|---|---|---|
| `GOOGLE_API_KEY` | `.env` | Your Google Gemini API key |
| `SECRET_KEY` | `settings.py` | Django secret key (change in production!) |
| `DEBUG` | `settings.py` | Set to `False` in production |
| `ALLOWED_HOSTS` | `settings.py` | Add your domain in production |

<br>

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to branch (`git push origin feature/amazing-feature`)
5. 🔃 Open a Pull Request

<br>

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

<br>

---

<div align="center">

**Built with 💜 using Django & Google Gemini AI**

_If you found this useful, consider giving it a ⭐!_

</div>
