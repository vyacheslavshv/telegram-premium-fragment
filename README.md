# Telegram Premium Gifting Automation

Automate the process of gifting Telegram Premium subscriptions to specified usernames using ADB.

## Description

This Python script automates the process of gifting Telegram Premium subscriptions to a list of Telegram usernames. The automation is accomplished using Android Debug Bridge (ADB) to simulate user interactions on an Android device.

## Prerequisites

- Python 3.x
- ADB tools installed and set up
- A connected Android device with ADB debugging enabled
- Tonkeeper app installed and logged in on the device

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/vyacheslavshv/telegram-premium-gifting.git
   ```
2. Navigate to the project directory:
   ```
   cd telegram-premium-gifting
   ```
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Edit the `main.py` file and update the `usernames` list with the Telegram usernames to whom you want to gift the Premium subscription.
2. Run the script:
   ```
   python main.py
   ```

## Note

Ensure that your Android device is connected, ADB debugging is enabled, and the Tonkeeper app is open.