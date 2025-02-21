from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

# Configurable database file path
db_file = os.getenv("DB_FILE", "database.csv")


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
            save_to_csv(name, email, message)
            return redirect("/thank_you")

    return redirect("/")


@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")

# Function to save form data to CSV


def save_to_csv(name, email, message):
    try:
        with open(db_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([name, email, message])
    except Exception as e:
        print(f"Error writing to CSV: {e}")


if __name__ == "__main__":
    app.run(debug=True)
