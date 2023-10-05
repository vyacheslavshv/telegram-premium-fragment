# Telegram Premium Gifting Automation

This documentation provides instructions for setting up and running the Telegram Premium Gifting Automation tool. This server application has been developed to automate the process of gifting Telegram Premium subscriptions via ADB interactions with the Tonkeeper application.

## Requirements

- Python >= 3.9
- ADB tools properly installed and configured
- An Android device with ADB debugging enabled
- The Tonkeeper application installed and active on the device

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

## Configuration and Environment Variables

Before running the application, you need to set up your environment variables. These variables store your configuration settings, ensuring your setup is secure and transferable.

### Setting Up Environment Variables

1. **Using `.env.example`:** We provide a `.env.example` file to showcase what environment variables need to be defined. This file contains dummy values and serves as a template.
   
   Example `.env.example` file:
   ```plaintext
   API_KEY=YOUR_ACTUAL_SECRET_API_KEY
   ```
   
2. **Creating `.env`:** Duplicate `.env.example` and rename it to `.env`. Replace `YOUR_ACTUAL_SECRET_API_KEY` with your real API key.
   
   Example `.env` file:
   ```plaintext
   API_KEY=abcdefgh1234567890ijklmnopqrstuv
   ```

### Using the API Key

The API key stored in your `.env` file is used to authenticate requests to your API. Ensure you include it in your requests as a header.

Example Request Header:
```plaintext
x-api-key: abcdefgh1234567890ijklmnopqrstuv
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