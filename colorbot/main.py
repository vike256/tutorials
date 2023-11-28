"""
    Simple colorbot by vike256
    Consider donating: https://github.com/vike256#donations

    Press F1 to exit the program
    Hold Left Ctrl to activate triggerbot
    Hold right mouse button to activate aimbot
"""

import cv2
import win32api
import win32con
import numpy as np
from time import sleep
from mss import mss


# Configuration
FOV_X = 256  # FOV width
FOV_Y = 256  # FOV height
SPEED = 1  # Movement speed
UPPER_COLOR = np.array([63, 255, 255])  # Upper bound of the color range to target
LOWER_COLOR = np.array([58, 210, 80])  # Lower bound of the color range to target


# Defining a function that moves the mouse according to the given x and y value
def mouse_move(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)


# Simulates a left mouse click. Waits for 0.04 seconds to simulate a natural click.
def mouse_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def main():
    # Initialize the MSS screenshot capture tool
    camera = mss()

    # Get the screen dimensions and calculate the center coordinates
    screen_area = (camera.monitors[1]['width'], camera.monitors[1]['height'])
    screen_center = (screen_area[0] // 2, screen_area[1] // 2)

    # Define the field of view area and calculate its center coordinates
    fov_area = (FOV_X, FOV_Y)
    fov_center = (FOV_X // 2, FOV_Y // 2)

    # Calculate the region of the screen to capture for the field of view
    fov_region = (
        screen_center[0] - fov_area[0] // 2,
        screen_center[1] - fov_area[1] // 2,
        screen_center[0] + fov_area[0] // 2,
        screen_center[1] + fov_area[1] // 2
    )

    print('Start')

    # The main program loop
    while True:
        # Check if the F1 key is pressed to exit the loop
        if win32api.GetAsyncKeyState(win32con.VK_F1) < 0:
            break

        # Capture a screenshot of the field of view region
        while True:
            screenshot = camera.grab(fov_region)
            if screenshot is not None:
                screenshot = np.array(screenshot)
                break

        # Reset variables for each iteration
        target = (0, 0)  # Target coordinates
        trigger = False  # Flag indicating whether to click
        closest_target = None  # Variable to store the closest target contour

        # Convert the screenshot to HSV color space for color detection
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

        # Create a mask to identify pixels within the specified color range
        mask = cv2.inRange(hsv, LOWER_COLOR, UPPER_COLOR)

        # Apply morphological dilation to increase the size of the detected color blobs
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)

        # Apply thresholding to convert the mask into a binary image
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]

        # Find contours of the detected color blobs
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Identify the closest target contour
        if len(contours) != 0:
            min_distance = float('inf')
            for contour in contours:
                # Make a bounding rectangle for the target
                rect_x, rect_y, rect_w, rect_h = cv2.boundingRect(contour)

                # Calculate the coordinates of the center of the target
                x = rect_x + rect_w // 2 - fov_center[0]
                y = rect_y + rect_h // 2 - fov_center[1]

                # Update the closest target if the current target is closer
                distance = np.sqrt(x**2 + y**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_target = contour
                    target = (x, y)

            # Check if the closest target is at the center of the screen
            if closest_target is not None:
                if cv2.pointPolygonTest(closest_target, fov_center, False) >= 0:
                    trigger = True

        # Calculate the movement values based on the target coordinates
        move_x = target[0] * SPEED
        move_y = target[1] * SPEED

        # Click if target at the center of the screen and left Ctrl is pressed
        if trigger and win32api.GetAsyncKeyState(win32con.VK_LCONTROL) < 0:
            mouse_click()
            print('Click')

        # Move if target outside the center of the screen and right mouse button pressed
        if win32api.GetAsyncKeyState(win32con.VK_RBUTTON) < 0 and (move_x != 0 or move_y != 0):
            mouse_move(move_x, move_y)
            print(f'Move {move_x}, {move_y}')

    print('Exit')


if __name__ == '__main__':
    main()
