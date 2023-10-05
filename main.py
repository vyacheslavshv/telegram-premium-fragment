import threading
import queue
import os
from flask import Flask, request, jsonify
from adb_utils import AdbAutomation
from telegram_gifting import gift_premium
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
API_KEY = os.getenv("API_KEY")
task_queue = queue.Queue()


def worker():
    """Background worker that processes tasks."""
    while True:
        task = task_queue.get()
        if task is None:
            break
        try:
            automation = AdbAutomation()
            gift_premium(automation, task)
        except Exception as e:
            print(f"Error processing task for {task}: {str(e)}")
        task_queue.task_done()


worker_thread = threading.Thread(target=worker)
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
    try:
        app.run(host="0.0.0.0", port=80)
    finally:
        # Ensure all tasks are completed before exiting
        task_queue.join()
        # Stop the worker thread
        task_queue.put(None)
        worker_thread.join()
