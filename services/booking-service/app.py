from flask import Flask,jsonify,request
from flask_cors import CORS
from datetime import datetime,timezone
import sqlite3,os
from pathlib import Path
app=Flask(__name__); CORS(app)
DB=os.getenv("DB_PATH","/data/bookings.db")
VALID_RIDES={"bike","auto","cab"}
Path(DB).parent.mkdir(parents=True,exist_ok=True)
def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.execute("CREATE TABLE IF NOT EXISTS ride_bookings(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,phone TEXT NOT NULL,pickup TEXT NOT NULL,destination TEXT NOT NULL,ride_type TEXT NOT NULL,distance_km REAL NOT NULL,estimated_fare INTEGER NOT NULL,status TEXT NOT NULL,created_at TEXT NOT NULL)")
    c.commit(); return c
@app.get("/health")
def health(): c=conn(); c.close(); return jsonify(status="healthy",service="booking-service")
@app.post("/bookings")
def create():
    d=request.get_json(silent=True) or {}
    req=["name","phone","pickup","destination","ride_type","distance_km","estimated_fare"]
    miss=[x for x in req if not str(d.get(x,"")).strip()]
    if miss:return jsonify(error="Missing: "+", ".join(miss)),400
    if d["ride_type"] not in VALID_RIDES:return jsonify(error="Unsupported ride type"),400
    try: distance,fare=float(d["distance_km"]),int(d["estimated_fare"])
    except (TypeError,ValueError): return jsonify(error="Invalid distance or fare"),400
    if not 0.5<=distance<=100 or fare<1:return jsonify(error="Invalid trip details"),400
    c=conn(); cur=c.execute("INSERT INTO ride_bookings(name,phone,pickup,destination,ride_type,distance_km,estimated_fare,status,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
      (d["name"].strip(),d["phone"].strip(),d["pickup"].strip(),d["destination"].strip(),d["ride_type"],distance,fare,"confirmed",datetime.now(timezone.utc).isoformat()))
    c.commit(); bid=cur.lastrowid; c.close()
    return jsonify(message="Ride confirmed. Your captain is being assigned!",booking_id=bid,status="confirmed"),201
app.run(host="0.0.0.0",port=int(os.getenv("PORT","5002")))
