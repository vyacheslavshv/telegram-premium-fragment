import requests

API_URL = "http://ip:port/gift"
API_KEY = "YOU_API_KEY"


def send_request(usernames):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "usernames": usernames
    }

    response = requests.post(API_URL, headers=headers, json=data)
    print(response.json())


if __name__ == "__main__":
    usernames_to_gift = ["@username"]
    send_request(usernames_to_gift)
