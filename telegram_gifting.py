import pytesseract
from time import sleep
from fuzzywuzzy import fuzz

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 2220


def gift_premium(automation, username):
    """
    Gifts a premium subscription to a specified Telegram username.
    """

    # Ensure we're on the right screen before proceeding
    while not wait_for_correct_screen(automation, "Buy Telegram Premium"):
        handle_failure(automation)

    # Tap on the cancel cross
    for _ in range(2):
        automation.tap(SCREEN_WIDTH * 0.95, SCREEN_HEIGHT * 0.4)
        sleep(0.5)

    # Tap to enter username
    automation.tap(SCREEN_WIDTH * 0.95, SCREEN_HEIGHT * 0.4)
    sleep(0.7)

    # Insert username
    automation.input_text(username)
    sleep(0.7)

    # Confirm username
    automation.press_keyevent(66)
    sleep(0.7)

    # Take a screenshot to check for specific messages
    screenshot = automation.take_screenshot()

    if is_desired_screen(screenshot, "No Telegram users found."):
        save_unsuccessful_username(username)
        print(f"Skipping: No Telegram users found for username {username}")
        return

    if is_desired_screen(screenshot, "This account is already subscribed to Telegram Premium."):
        save_unsuccessful_username(username)
        print(f"Skipping: The account {username} is already subscribed to Telegram Premium.")
        return

    # Tap on "6 month"
    for _ in range(2):
        automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.6)
        sleep(0.35)

    # Tap on "Gift Telegram Premium"
    if not tap_and_verify(
        automation, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.76,
        "Gift Telegram Premium", 3
    ):
        save_unsuccessful_username(username)
        handle_failure(automation)
        return

    # Tap on "Buy Gift for {username}"
    if not tap_and_verify(
        automation, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.9,
        "Scan the QR code", 2
    ):
        save_unsuccessful_username(username)
        handle_failure(automation)
        return

    # Tap on "Buy Premium with Tonkeeper"
    if not tap_and_verify(
        automation, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85,
        "Confirm action", 2
    ):
        save_unsuccessful_username(username)
        handle_failure(automation)
        return

    # Tap on "Confirm"
    if not tap_and_verify(
        automation, SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.9,
        "Enter passcode", 2
    ):
        save_unsuccessful_username(username)
        handle_failure(automation)
        return

    # Tap on "Passcode"
    for _ in range(4):
        automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.65)
        sleep(0.5)
    sleep(10)

    # # Open "Tonkeeper" again
    # automation.start_app("com.ton_keeper", ".MainActivity")
    # sleep(5)

    if not wait_for_correct_screen(automation, "Gift Sent!", msg=False):
        save_unsuccessful_username(username)
        handle_failure(automation)
        return

    # Tap on "Send another gift"
    if not tap_and_verify(
        automation, SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.7,
        "Premium Giveaways", 2
    ):
        save_unsuccessful_username(username)
        handle_failure(automation)
        return

    # Tap on "Buy Premium for a User"
    automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.6)
    sleep(2)

    # Tap for return
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.25)


def wait_for_correct_screen(automation, expected_text, msg=True, iterations=50):
    message_displayed = False
    iteration_count = 0
    while True:
        iteration_count += 1

        # Take a screenshot
        screenshot = automation.take_screenshot()

        # Check if it's the desired screen
        if is_desired_screen(screenshot, expected_text):
            if message_displayed and msg:
                print("\033[92mSuccessfully found the desired screen: '{}'\033[0m".format(expected_text))
            sleep(1)
            return True

        if iteration_count > iterations:
            print(f"Failed to find the '{expected_text}' screen within {iterations*2} seconds.")
            return False

        if not message_displayed and msg:
            print(f"Waiting for the '{expected_text}' screen to appear...")
            message_displayed = True

        sleep(1)


def handle_failure(automation):
    # Open "Tonkeeper" again
    # automation.start_app("com.ton_keeper", ".MainActivity")
    # sleep(2)

    # Tap for return
    for _ in range(3):
        automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.25)
        sleep(1)

    # Tap on reload
    for _ in range(2):
        automation.tap(SCREEN_WIDTH * 0.77, SCREEN_HEIGHT * 0.07)
        sleep(1)

    # Tap on "Send another gift"
    tap_and_verify(
        automation, SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.7,
        "Premium Giveaways", 2
    )

    # Tap on "Buy Premium for a User"
    automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.6)
    sleep(2)


def tap_and_verify(automation, x, y, expected_screen, wait_time=1, retry_limit=3):
    """
    Attempts to tap on a coordinate and verify if the expected screen is reached.
    Retries a limited number of times if unsuccessful.
    """
    for attempt in range(retry_limit):
        automation.tap(x, y)
        sleep(wait_time)

        if wait_for_correct_screen(automation, expected_screen, msg=False, iterations=10):
            return True

    return False


def get_screen_text(image):
    return pytesseract.image_to_string(image)


def is_desired_screen(image, expected_text, similarity_threshold=90):
    screen_text = get_screen_text(image)
    similarity = fuzz.partial_ratio(screen_text, expected_text)
    return similarity >= similarity_threshold


def save_unsuccessful_username(username, filename="unsuccessful_usernames.txt"):
    with open(filename, "a") as f:
        f.write(username + "\n")
