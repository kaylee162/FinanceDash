# 💰 FinanceDash — Personal Financial Dashboard

**FinanceDash** is a full-stack **Flask** web application that helps users track income, expenses, and budgets in one interactive dashboard.
It visualizes financial data through clean charts and provides insights into spending habits — helping users make smarter money decisions.

## 🚀 Features

✅ **User Authentication** – Secure signup/login using Flask-Login  
✅ **Transaction Management** – Add, edit, and delete income or expense entries  
✅ **Budget Tracking** – Create and monitor category-based budgets  
✅ **Interactive Dashboard** – View dynamic charts summarizing financial data  
✅ **Categorization** – Tag transactions (Food, Rent, Travel, etc.) for better analysis  
✅ **Persistent Storage** – SQLite or PostgreSQL database support  
✅ **Responsive UI** – Modern and mobile-friendly interface  

## 🧠 Tech Stack

| Layer           | Technology                                |
| --------------- | ----------------------------------------- |
| **Frontend**    | HTML, CSS, JavaScript, Bootstrap/Chart.js |
| **Backend**     | Python (Flask Framework)                  |
| **Database**    | SQLite (default) or PostgreSQL            |
| **Auth**        | Flask-Login                               |
| **Environment** | Python-Dotenv for config management       |

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/FinanceDash.git
cd FinanceDash
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create a `.env` File

```
FLASK_SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///finance.db
```

### 5️⃣ Initialize the Database

```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 6️⃣ Run the App

```bash
flask run
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser

## 📊 Dashboard Overview

The dashboard displays:

* **Total Income & Expenses**
* **Monthly Budget Overview**
* **Category Breakdown (Pie Chart)**
* **Spending Trends Over Time (Line Chart)**

Users can easily filter data by date or category.

## 🧩 Project Structure

```
FinanceDash/
│
├── app.py                  # Flask app factory
├── extensions.py            # DB and Login manager setup
├── models.py                # User & Transaction models
├── models_budget.py         # Budget model
├── routes_auth.py           # Auth routes
├── routes_dashboard.py      # Dashboard and transaction logic
│
├── templates/               # HTML templates (Jinja2)
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   └── budget.html
│
├── static/                  # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── img/
│
├── requirements.txt
└── .env.example
```

---

## 🧪 Future Enhancements

* 🔐 Two-factor authentication
* 📈 AI-based financial insights
* 💾 CSV import/export for transactions
* 💬 Email or SMS budget alerts

## 🧑‍💻 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Add feature"`)
4. Push and open a pull request

## 💡 Author

Developed by **Kaylee Henry**  
📧 Email: [kayleehenry162@gmail.com](mailto:kayleehenry162@gmail.com)
