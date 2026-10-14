# Sambhav's Store - E-Commerce Platform

A full-stack e-commerce web application built as an academic project for B.Sc. Computer Science. It features a complete MVC architecture, an interactive cart system, and a simulated secure checkout gateway.

**Author:** Sambhav Shilimkar

## 🚀 Tech Stack
*   **Backend:** Python 3, Flask
*   **Frontend:** HTML5, CSS3 (CSS Grid/Flexbox), Vanilla JavaScript
*   **Database:** SQLite3
*   **Architecture:** Model-View-Controller (MVC)

## ✨ Core Features
1.  **Dynamic Catalog:** Fetches and renders product data directly from the SQLite database.
2.  **Session-Based Cart:** Utilizes Flask server-side sessions to manage cart state without overloading the database.
3.  **Atomic Transactions:** The checkout process uses strict SQL transaction rollbacks to prevent inventory errors (e.g., deducting stock when a payment fails).
4.  **Responsive UI:** A modern interface with a slide-out cart sidebar, toast notifications, and a secure mock-payment modal form enforcing data validation via Regex.

## 📂 Project Structure
```text
fullstack_store/
├── app.py                 # Main Flask application and API routes
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── database/
│   ├── schema.sql         # SQL structure and initial inventory data
│   ├── init_db.py         # Script to initialize the database
│   └── store.db           # SQLite database file (generated automatically)
├── static/
│   ├── css/
│   │   └── style.css      # Custom styling, grid layout, and animations
│   └── js/
│       └── main.js        # DOM manipulation and asynchronous API fetching
└── templates/
    └── index.html         # Main user interface and modal forms
⚙️ Installation & Setup (Linux/WSL)
Create and activate a virtual environment:

Bash
python3 -m venv venv
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Initialize the database:

Bash
python3 database/init_db.py
Run the server:

Bash
python3 app.py
View the application:
Open a web browser and navigate to http://127.0.0.1:5000.
