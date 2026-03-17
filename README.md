# 🍽️ Macro Tracker API

A FastAPI-based backend project to track foods, meals, and nutritional macros like **fat, protein, and carbohydrates**.

---
## 🌐 Live API

🚀 Deployed on Render:

👉 https://fastapi-macro-tracker.onrender.com/docs

### 📖 API Docs

* Swagger UI → https://fastapi-macro-tracker.onrender.com/docs
* ReDoc → https://fastapi-macro-tracker.onrender.com/redoc

---

## 📌 Features

* 👤 User management (Authentication in progress 🔐)
* 🍎 Food tracking (fat, protein, carbs)
* 🍽️ Meal management
* 🗄️ Database integration with SQLAlchemy
* ⚡ FastAPI for high-performance APIs

---

## 🚧 Current Status

> ⚙️ Authentication system is currently in progress
> (password hashing, login, and secure endpoints)

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Database:** SQLite / PostgreSQL (configurable)
* **ORM:** SQLAlchemy
* **Validation:** Pydantic
* **Auth (WIP):** Passlib (bcrypt)

---

## 📂 Project Structure

app/
├── models.py        # SQLAlchemy models
├── schemas.py       # Pydantic schemas
├── crud.py          # Database operations
├── apis/            # API routes
├── deps.py          # Dependencies
└── main.py          # Entry point

---

## 🚀 Getting Started

### 1️⃣ Clone the repo

```bash
git clone https://github.com/Ravikalakoti/fastapi-macro-tracker.git
cd fastapi-macro-tracker
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the server

```bash
uvicorn app.main:app --reload
```

---

## 📖 API Docs

After running the server, visit:

* Swagger UI → http://127.0.0.1:8000/docs
* ReDoc → http://127.0.0.1:8000/redoc

---

## 🎯 Future Improvements

* 🔐 Complete authentication (JWT login/signup)
* 📊 Macro analytics
* 📅 Daily meal tracking
* 🌐 Deployment (Render / AWS)

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a pull request.

---

## 📧 Contact

**Ravi Kalakoti**
📩 [ravikalakoti16@gmail.com](mailto:ravikalakoti16@gmail.com)

---

⭐ If you like this project, give it a star!
