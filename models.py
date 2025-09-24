from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)   # store hashed password
    role = db.Column(db.String(20), nullable=False)  # 'commuter' or 'owner'

    parking_spots = db.relationship('ParkingSpot', backref='owner', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    timings = db.Column(db.String(255), nullable=False)  # e.g., "8:00-22:00"
    price_per_hour = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Boolean, default=True)

    # Relationships
    bookings = db.relationship('Booking', backref='parking_spot', lazy=True)

    # For maps
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<ParkingSpot {self.location} - {'Available' if self.availability else 'Unavailable'}>"


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='confirmed')  # confirmed, canceled, etc.
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
