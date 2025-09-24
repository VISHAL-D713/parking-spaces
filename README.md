# 🚗 Parking Web App

A simple **Parking Management Web App** built using **Flask, SQLAlchemy, HTML, CSS, and JavaScript**.  
This app helps manage parking slots, users, and bookings with a clean UI and backend integration.

---

## ✨ Features
- 🔐 User authentication (Register/Login)
- 🅿️ Manage parking slots (add, update, delete)
- 📅 Book & release parking slots
- 📊 Dashboard to view available/occupied slots
- 📱 Responsive frontend with HTML, CSS, JS
- 🗄️ Database integration using SQLAlchemy
- ☁️ Ready for deployment on **Render/Heroku**

---

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask (Python)  
- **Database:** SQLAlchemy (SQLite/PostgreSQL)  
- **Deployment:** Render / Heroku  

---

## 📂 Project Structure
```bash
parking_app/
├── static/            # CSS, JS, Images
├── templates/         # HTML templates
├── app.py             # Main Flask app
├── config.py          # Configuration file
├── models.py          # Database models
├── forms.py           # Forms handling
├── requirements.txt   # Python dependencies
├── Procfile           # Deployment config
└── README.md          # Project documentation
````

---

## ⚡ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/chetanhire66/parking_app.git
   cd parking_app
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Mac/Linux
   venv\Scripts\activate       # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

5. **Run the app**

   ```bash
   flask run
   ```

6. Open in browser → [[http://127.0.0.1:5000](http://127.0.0.1:5000)](https://parking-app-va6k.onrender.com/all_spots)

---

## 🚀 Deployment

The app is ready for deployment on **Render/Heroku**.

* Ensure `Procfile` and `requirements.txt` are present.
* Push code to GitHub.
* Connect repo to Render/Heroku.
* Deploy and enjoy! 🎉

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify.
