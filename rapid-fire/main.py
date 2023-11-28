"""
    Simple rapid-fire script by vike256
    This script simulates rapid-fire clicking by repeatedly clicking the left mouse button at a specified frequency.
    Consider donating: https://github.com/vike256#donations
"""
import win32api  # Import the win32api library to interact with the Windows API
import win32con  # Import the win32con library for Windows constants
import time  # Import the time library for timing operations

# Define constants for the desired clicks per second and the rapid-fire key
CLICKS_PER_SECOND = 20  # Number of clicks to simulate per second
RAPID_FIRE_KEY = win32con.VK_SPACE  # Keybind for rapid-fire

# Initialize a global variable to track the last click time
last_click_time = time.time()


# Simulates a left mouse click
def mouse_click():
    global last_click_time

    # Update the last click time
    last_click_time = time.time()

    # Simulate pressing and releasing the left mouse button
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    # Print a message indicating a click has been simulated
    print('Click')


# Define the main program loop
def main():
    global last_click_time

    print('Start')
    while True:
        # Check if the F1 key is pressed to exit the loop
        if win32api.GetAsyncKeyState(win32con.VK_F1) < 0:
            break

        # Check if the rapid-fire key is held down and it's time to simulate another click
        if (
            win32api.GetAsyncKeyState(RAPID_FIRE_KEY) < 0 and
            time.time() >= last_click_time + 1 / CLICKS_PER_SECOND
        ):
            mouse_click()

        # Otherwise, sleep for a short period to avoid unnecessary processing
        else:
            time.sleep(0.01)

    print('Exit')


# Run the main program
if __name__ == '__main__':
    main()
