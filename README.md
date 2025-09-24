🚗 Parking Web App

A smart Parking Management Web App built using Flask, SQLAlchemy, HTML, CSS, and JavaScript.
This app helps manage parking slots, users, and bookings with a clean UI and integrated backend.

✨ Features

🔐 User Authentication – Register and login functionality.

🅿️ Manage Parking Slots – Add, update, and delete slots.

📅 Book & Release Slots – Users can reserve or release parking slots easily.

📊 Dashboard – View available and occupied parking slots.

📱 Responsive Design – Works on desktop and mobile devices.

🗄️ Database Integration – Uses SQLAlchemy with SQLite/PostgreSQL backend.

☁️ Ready for Deployment – Can be deployed on Render or Heroku.

🛠️ Tech Stack

Frontend: HTML, CSS, JavaScript

Backend: Flask (Python)

Database: SQLAlchemy (SQLite/PostgreSQL)

Deployment: Render / Heroku

📂 Project Structure
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

⚡ Installation & Setup

Clone this repository:

git clone https://github.com/VISHAL-D713/parking-spaces.git
cd parking-spaces


Create a virtual environment:

python3 -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows


Install dependencies:

pip install -r requirements.txt


Set up the database:

flask db init
flask db migrate -m "Initial migration."
flask db upgrade


Run the app:

flask run


Open in browser → http://127.0.0.1:5000
Deployed link ->  https://parking-app-va6k.onrender.com/all_spots



Developed for TENET Hackathon 2025.

📜 License

This project is licensed under the MIT License – free to use and modify.
