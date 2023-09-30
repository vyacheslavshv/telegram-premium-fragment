# Telegram Premium Gifting Automation

This documentation provides instructions for setting up and running the Telegram Premium Gifting Automation tool. This server application has been developed to automate the process of gifting Telegram Premium subscriptions via ADB interactions with the Tonkeeper application.

## Requirements

- Python >= 3.9
- ADB tools properly installed and configured
- An Android device with ADB debugging enabled
- The Tonkeeper application installed and active on the device

## Project Files

```
- adb_utils.py          : Contains utility functions for ADB interactions.
- client_request.py     : Demonstrates the correct method to structure client requests to the server.
- main.py               : The central server script.
- telegram_gifting.py   : Handles the automation of the gifting process.
- requirements.txt      : Specifies required Python packages.
- README.md             : This documentation file.
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vyacheslavshv/telegram-premium-fragment.git
   ```

2. Move to the project directory:
   ```bash
   cd telegram-premium-fragment
   ```

3. Install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The tool runs as a Flask server, which responds to incoming API requests to commence the gifting operation.

To start the server:
   ```bash
   python main.py
   ```

When you need guidance on how to frame the API requests to the server, please consult `client_request.py`.

## Important Reminders

Before deploying the server:
- Confirm that the Android device is connected and recognized.
- Ensure that ADB debugging is active on the device.
- Ensure that the Tonkeeper app is operational and logged in.