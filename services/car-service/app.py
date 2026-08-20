from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
RIDES = [
    {"id":"bike","name":"Bike","subtitle":"Fastest way through traffic","capacity":1,"eta":"3 min","base_fare":25,"per_km":8,"image":"https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=900&q=80"},
    {"id":"auto","name":"Auto","subtitle":"Everyday rides, fairly priced","capacity":3,"eta":"5 min","base_fare":35,"per_km":11,"image":"https://images.unsplash.com/photo-1565610222536-ef125c59da2e?auto=format&fit=crop&w=900&q=80"},
    {"id":"cab","name":"Cab","subtitle":"Comfort for the whole crew","capacity":4,"eta":"7 min","base_fare":60,"per_km":16,"image":"https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=900&q=80"}]

@app.get("/health")
def health(): return jsonify(status="healthy", service="ride-service")
@app.get("/rides")
def rides(): return jsonify(RIDES)
@app.get("/estimate")
def estimate():
    ride_id = request.args.get("ride_type", "bike")
    try: distance = float(request.args.get("distance_km", "4"))
    except ValueError: return jsonify(error="distance_km must be a number"), 400
    if not 0.5 <= distance <= 100: return jsonify(error="distance_km must be between 0.5 and 100"), 400
    item = next((ride for ride in RIDES if ride["id"] == ride_id), None)
    if not item: return jsonify(error="Ride type not found"), 404
    return jsonify(ride_type=ride_id, distance_km=distance, estimated_fare=round(item["base_fare"] + item["per_km"] * distance), currency="INR", eta=item["eta"])

app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5001")))
