from flask import Flask, render_template, request, redirect
import os
import json
from datetime import datetime

app = Flask(__name__)

# Create a data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Path to the JSON file
JSON_FILE = 'data/form_submissions.json'

# Initialize JSON file if it doesn't exist
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w') as f:
        json.dump([], f)

@app.route("/")
def portfolio():
    return render_template("index.html")

@app.route("/submit_form", methods=["POST"])
def submit_form():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if name and email and message:
            save_to_json(name, email, message)
            return redirect("/thank_you")

    return redirect("/")

@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")

def save_to_json(name, email, message):
    try:
        # Read existing data
        with open(JSON_FILE, 'r') as f:
            submissions = json.load(f)
        
        # Create new submission entry
        new_submission = {
            'name': name,
            'email': email,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Append new submission
        submissions.append(new_submission)
        
        # Write back to file
        with open(JSON_FILE, 'w') as f:
            json.dump(submissions, f, indent=4)
            
    except Exception as e:
        print(f"Error while saving to JSON: {e}")

if __name__ == "__main__":
    app.run(debug=True)
