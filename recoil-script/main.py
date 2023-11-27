"""
    Simple recoil script by vike256
    Consider donating: https://github.com/vike256#donations
"""
import win32api  # Import the win32api library to interact with the Windows API
import win32con  # Import the win32con library for Windows constants
import time  # Import the time library for timing operations

# Define constants for recoil values and delay
RECOIL_X = 0  # Horizontal recoil value
RECOIL_Y = 10  # Vertical recoil value
DELAY = 10  # Delay in milliseconds between adjustments


# Defining a function that moves the mouse according to the given x and y value
def mouse_move(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
    print(f'Move {x}, {y}')


# Define the main program loop
def main():
    # The main program loop
    while True:
        # Check if the F1 key is pressed to exit the loop
        if win32api.GetAsyncKeyState(win32con.VK_F1) < 0:
            break

        # Check if the left mouse button is clicked to trigger recoil adjustment
        if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0:
            mouse_move(RECOIL_X, RECOIL_Y)  # Send mouse input based on recoil values

        time.sleep(DELAY / 1000)  # Delay between adjustments


# Run the main program
if __name__ == '__main__':
    main()
