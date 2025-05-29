# 📚 Study Materials Management System

A web-based application to manage, organize, and share academic materials efficiently. Developed using **Flask**, **HTML/CSS**, and **MySQL**, this system enables users to upload, update, delete, and view study materials with ease.

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0.2-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

---

## 🔗 Live Demo

🔴 [Live on Railway](https://study-materials-management-system.up.railway.app/)

---

## 📌 Features

- 🧑‍💼 **User Authentication** (Login & Registration)
- 📝 **Add, Update, and Delete** study materials
- 📦 **Order and Item Management** (material name, unit, price)
- 📊 **Material Status Tracking** (availability, total count)
- 🧾 **Track Orders** (date, customer name, total cost)
- 🔐 Authentication-protected routes

---

## 🛠️ Technologies Used

| Category       | Stack                             |
|----------------|-----------------------------------|
| **Frontend**   | HTML5, CSS3, Bootstrap             |
| **Backend**    | Python, Flask                      |
| **Database**   | MySQL                              |
| **Deployment** | Railway                            |

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/MNR-Tushar/Study-Materials-Management-System.git
cd Study-Materials-Management-System
```
### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the Database
Create a MySQL database.
Update database credentials in app.py or use environment variables for security.

### 5. Run the Application
```bash
python app.py
```
Visit: http://127.0.0.1:5000/ in your browser.

---
### 📁 Project Structure
```bash
Study-Materials-Management-System/
│
├── static/               # CSS, Images
├── templates/            # HTML templates
├── app.py                # Main Flask app
├── requirements.txt      # Python dependencies
├── Procfile              # For Railway Deployment
└── README.md             # Project documentation
```
---
### 🚀 Deployment
This project is deployed on Railway. To deploy your own version:
Create a Railway account.
Connect your GitHub repo.
Set environment variables for your DB credentials.
Deploy and preview live!

---
### 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

---
### ❤️ Contributions
Contributions, issues, and feature requests are welcome!
Feel free to fork the repo and submit a pull request.
```bash
Let me know if you'd like to include screenshots, update author info, or add database schema instructions. I can also help you automate a deployment or Dockerize the app if needed.
```

