from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import base64
import cv2
import numpy as np

from helmet_detector import check_ppe_ai

app = Flask(__name__)

# ---------------- Dashboard / Home ----------------
@app.route('/')
def home():
    prompts = [
        "Check your PPE before starting work.",
        "Ensure machinery is properly guarded.",
        "Follow roof support guidelines strictly."
    ]
    return render_template('index.html', prompts=prompts)


# ---------------- Videos ----------------
@app.route('/videos')
def videos():
    return render_template('videos.html')


# ---------------- Checklist ----------------
@app.route('/checklist', methods=['GET', 'POST'])
def checklist():
    tasks = [
        "Wear helmet", "Wear gloves", "Wear safety shoes", "Wear goggles",
        "Check machinery condition", "Check electrical wiring safety",
        "Confirm tools are properly stored",
        "Fire extinguisher available",
        "First aid kit available",
        "Emergency exit accessible",
        "Proper ventilation available"
    ]

    if request.method == 'POST':
        completed = request.form.getlist('tasks')
        print("Completed:", completed)
        return redirect(url_for('checklist'))

    return render_template('checklist.html', tasks=tasks)


# ---------------- PPE Scan ----------------
@app.route('/scan')
def scan():
    detected, missing = check_ppe_ai()

    if not missing:
        return """
        <h2 style='color:green'>✅ All Safety Gear Detected</h2>
        <h3>ENTRY ALLOWED</h3>
        <a href="/">Back</a>
        """
    else:
        missing_html = "".join(
            f"<li>{item.replace('_', ' ').title()}</li>" for item in missing
        )
        return f"""
        <h2 style='color:red'>❌ Safety Violation</h2>
        <ul>{missing_html}</ul>
        <h3>ENTRY DENIED</h3>
        <a href="/">Back</a>
        """


# ---------------- Hazard Report ----------------
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        name = request.form['name']
        hazard = request.form['hazard']
        file = request.files.get('file')

        filename = None
        if file:
            filename = file.filename
            file.save(f'static/uploads/{filename}')

        conn = sqlite3.connect("mine_safety.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO hazards (name, hazard, image) VALUES (?, ?, ?)",
            (name, hazard, filename)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('report'))

    return render_template('report.html')


if __name__ == "__main__":
    print("🚀 Starting Mine Safety Flask App...")
    app.run(debug=True)
