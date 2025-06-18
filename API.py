from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.INFO, filename="status.log", filemode="w",
                    format="[%(asctime)s] - %(filename)s - %(levelname)s | %(message)s")

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

@app.route('/', methods=['POST'])
def receive_data():
    auth_header = request.headers.get("Authorization")

    if auth_header != API_KEY:
        logging.warning(f"Unauthorized API connection detected using header {auth_header} while ours is {API_KEY}")
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    logging.info(data)

    return ({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True, port="5000", host="0.0.0.0")

