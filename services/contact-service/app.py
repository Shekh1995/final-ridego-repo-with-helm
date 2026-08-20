from flask import Flask,jsonify,request
from flask_cors import CORS
from datetime import datetime
import sqlite3,os
from pathlib import Path
app=Flask(__name__); CORS(app)
DB=os.getenv("DB_PATH","/data/contact.db")
Path(DB).parent.mkdir(parents=True,exist_ok=True)
def conn():
    c=sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT,message TEXT,created_at TEXT)")
    c.commit(); return c
@app.get("/health")
def health(): c=conn(); c.close(); return jsonify(status="healthy",service="contact-service")
@app.post("/contact")
def contact():
    d=request.get_json(silent=True) or {}
    for k in ["name","email","message"]:
        if not str(d.get(k,"")).strip(): return jsonify(error=f"{k} is required"),400
    c=conn(); c.execute("INSERT INTO messages(name,email,message,created_at) VALUES(?,?,?,?)",(d["name"],d["email"],d["message"],datetime.utcnow().isoformat())); c.commit(); c.close()
    return jsonify(message="Thanks. Our team will contact you shortly."),201
app.run(host="0.0.0.0",port=int(os.getenv("PORT","5003")))
