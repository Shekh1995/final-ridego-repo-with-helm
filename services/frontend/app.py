from flask import Flask,jsonify,request,render_template
import requests,os
app=Flask(__name__)
CAR=os.getenv("CAR_URL","http://car-service:5001"); BOOK=os.getenv("BOOKING_URL","http://booking-service:5002"); CONTACT=os.getenv("CONTACT_URL","http://contact-service:5003")
@app.get("/")
def home(): return render_template("index.html")
@app.get("/health")
def health():
    # Liveness must not depend on downstream services: otherwise a temporary
    # dependency outage restarts a healthy frontend container.
    return jsonify(status="healthy",service="frontend")
@app.get("/ready")
def ready():
    ok=True; checks={}
    for n,u in [("cars",CAR),("booking",BOOK),("contact",CONTACT)]:
        try: checks[n]=requests.get(u+"/health",timeout=2).ok
        except requests.RequestException: checks[n]=False
        ok &= checks[n]
    return jsonify(status="healthy" if ok else "degraded",dependencies=checks),200 if ok else 503
@app.get("/api/rides")
def rides():
    try:
        r=requests.get(CAR+"/rides",params=request.args,timeout=5); return r.text,r.status_code,{"Content-Type":"application/json"}
    except requests.RequestException as e:return jsonify(error="Car service unavailable",detail=str(e)),503
@app.get("/api/estimate")
def estimate():
    try:
        r=requests.get(CAR+"/estimate",params=request.args,timeout=5); return r.text,r.status_code,{"Content-Type":"application/json"}
    except requests.RequestException as e:return jsonify(error="Ride service unavailable",detail=str(e)),503
@app.post("/api/bookings")
def booking():
    try:
        r=requests.post(BOOK+"/bookings",json=request.get_json(silent=True),timeout=5); return r.text,r.status_code,{"Content-Type":"application/json"}
    except requests.RequestException as e:return jsonify(error="Booking service unavailable",detail=str(e)),503
@app.post("/api/contact")
def contact():
    try:
        r=requests.post(CONTACT+"/contact",json=request.get_json(silent=True),timeout=5); return r.text,r.status_code,{"Content-Type":"application/json"}
    except requests.RequestException as e:return jsonify(error="Contact service unavailable",detail=str(e)),503
app.run(host="0.0.0.0",port=int(os.getenv("PORT","8080")))
