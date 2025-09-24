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
