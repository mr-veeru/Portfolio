from flask import Flask, render_template, request, redirect
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


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
            save_to_mysql(name, email, message)
            return redirect("/thank_you")

    return redirect("/")


@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")


def save_to_mysql(name, email, message):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='portfolio',
            user='root',
            password='root'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            sql_insert_query = """INSERT INTO form_data (name, email, message) VALUES (%s, %s, %s)"""
            cursor.execute(sql_insert_query, (name, email, message))
            connection.commit()
            cursor.close()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)
