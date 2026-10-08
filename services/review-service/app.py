from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)


def get_connection():

    return mysql.connector.connect(
        host=os.getenv(
            "MYSQL_HOST",
            "review-mysql"
        ),
        user=os.getenv(
            "MYSQL_USER",
            "reviews"
        ),
        password=os.getenv(
            "MYSQL_PASSWORD",
            "reviews123"
        ),
        database=os.getenv(
            "MYSQL_DATABASE",
            "reviewsdb"
        )
    )


@app.route("/")
def home():

    return jsonify({
        "service": "Review Service",
        "status": "running"
    })


@app.route("/health")
def health():

    return jsonify({
        "service": "review-service",
        "status": "UP"
    })


@app.route("/reviews")
def reviews():

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute(
        "SELECT * FROM reviews"
    )

    result = cursor.fetchall()

    cursor.close()

    connection.close()

    return jsonify(result)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=3006
    )