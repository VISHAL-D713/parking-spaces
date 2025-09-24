from flask import Flask, render_template, redirect, url_for, flash, request, session, abort
from config import Config
from models import db, User, ParkingSpot, Booking
from forms import RegistrationForm, LoginForm, ParkingSpotForm, BookingForm
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

# -------------------- Login required decorator --------------------
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# -------------------- HOME --------------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

# -------------------- REGISTER --------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('login'))

        user = User(
            name=form.name.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# -------------------- LOGIN --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['role'] = user.role
            flash(f'Welcome, {user.name}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# -------------------- OWNER ROUTES --------------------
@app.route('/add_parking', methods=['GET', 'POST'])
@login_required(role='owner')
def add_parking():
    form = ParkingSpotForm()
    if form.validate_on_submit():
        spot = ParkingSpot(
            owner_id=session['user_id'],
            location=form.location.data,
            timings=form.timings.data,
            price_per_hour=form.price_per_hour.data,
            availability=form.availability.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data
        )
        db.session.add(spot)
        db.session.commit()
        flash('Parking spot added successfully.', 'success')
        return redirect(url_for('manage_listings'))
    return render_template('add_parking.html', form=form)

@app.route('/manage_listings')
@login_required(role='owner')
def manage_listings():
    spots = ParkingSpot.query.filter_by(owner_id=session['user_id']).all()
    return render_template('manage_listings.html', spots=spots)

@app.route('/edit_parking/<int:spot_id>', methods=['GET', 'POST'])
@login_required(role='owner')
def edit_parking(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.owner_id != session['user_id']:
        abort(403)
    form = ParkingSpotForm(obj=spot)
    if form.validate_on_submit():
        spot.location = form.location.data
        spot.timings = form.timings.data
        spot.price_per_hour = form.price_per_hour.data
        spot.availability = form.availability.data
        spot.latitude = form.latitude.data
        spot.longitude = form.longitude.data
        db.session.commit()
        flash('Listing updated.', 'success')
        return redirect(url_for('manage_listings'))
    return render_template('add_parking.html', form=form, edit=True)

@app.route('/delete_parking/<int:spot_id>', methods=['POST'])
@login_required(role='owner')
def delete_parking(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.owner_id != session['user_id']:
        abort(403)
    db.session.delete(spot)
    db.session.commit()
    flash('Listing deleted.', 'info')
    return redirect(url_for('manage_listings'))

# -------------------- COMMUTER ROUTES --------------------
@app.route('/search')
def search():
    query = request.args.get('query')
    spots = []
    if query:
        spots = ParkingSpot.query.filter(
            ParkingSpot.location.ilike(f'%{query}%'),
            ParkingSpot.availability == True
        ).all()
    return render_template('search.html', spots=spots, query=query)

@app.route('/parking/<int:spot_id>', methods=['GET', 'POST'])
@login_required(role='commuter')
def parking_details(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    form = BookingForm()
    if form.validate_on_submit():
        if form.start_time.data >= form.end_time.data:
            flash('End time must be after start time.', 'danger')
            return render_template('parking_details.html', spot=spot, form=form)
        booking = Booking(
            user_id=session['user_id'],
            parking_id=spot.id,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            status='confirmed'
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking confirmed!', 'success')
        return redirect(url_for('my_bookings'))
    return render_template('parking_details.html', spot=spot, form=form)

@app.route('/my_bookings')
@login_required(role='commuter')
def my_bookings():
    bookings = Booking.query.filter_by(user_id=session['user_id']).order_by(Booking.start_time.desc()).all()
    return render_template('bookings.html', bookings=bookings)

# -------------------- MAP AND ALL SPOTS --------------------
@app.route('/map_view')
def map_view():
    spots = ParkingSpot.query.filter_by(availability=True).all()
    spot_data = [
        {
            "id": spot.id,
            "location": spot.location,
            "lat": spot.latitude or 18.5204,
            "lng": spot.longitude or 73.8567,
            "price_per_hour": spot.price_per_hour,
            "timings": spot.timings,
            "availability": spot.availability,
            "owner_name": spot.owner.name,
        }
        for spot in spots
    ]
    return render_template('map_view.html', spots=spot_data)

@app.route('/all_spots')
def all_spots():
    spots = ParkingSpot.query.filter_by(availability=True).all()
    spot_data = [
        {
            "id": spot.id,
            "location": spot.location,
            "lat": spot.latitude or 18.5204,
            "lng": spot.longitude or 73.8567,
            "price_per_hour": spot.price_per_hour,
            "timings": spot.timings,
            "availability": spot.availability,
            "owner_name": spot.owner.name,
        }
        for spot in spots
    ]
    return render_template('all_spots.html', spots=spot_data)
# -------------------- RUN --------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)