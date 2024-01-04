import threading
import queue
import os
from flask import Flask, request, jsonify
from adb_utils import AdbAutomation
from telegram_gifting import gift_premium, save_unsuccessful_username
from dotenv import load_dotenv
from time import sleep

app = Flask(__name__)
load_dotenv()
API_KEY = os.getenv("API_KEY")
task_queue = queue.Queue()


def worker(device_id):
    """Background worker that processes tasks."""

    automation = AdbAutomation(device_id)
    while True:
        username = task_queue.get()
        try:
            gift_premium(automation, username)
        except Exception as e:
            save_unsuccessful_username(username)
            print(f"Error processing task for {username}: {e}")
            sleep(3)

        task_queue.task_done()


for device_number in range(1):
    worker_thread = threading.Thread(target=worker, args=(f'DEVICE_{device_number + 1}',))
    worker_thread.start()


@app.before_request
def limit_remote_addr():
    """API key verification."""
    if request.endpoint == 'gift_api' and request.headers.get("x-api-key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401


@app.route('/gift', methods=['POST'])
def gift_api():
    """Endpoint to gift premium subscription."""
    data = request.json

    # Validating the request data
    if not data or "usernames" not in data:
        return jsonify({"error": "usernames parameter is missing"}), 400

    usernames = data["usernames"]
    if not isinstance(usernames, list):
        return jsonify({"error": "usernames should be a list"}), 400

    for username in usernames:
        task_queue.put(username)

    return jsonify({"message": "Usernames have been added to the queue for gifting."}), 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
