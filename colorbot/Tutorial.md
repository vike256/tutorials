This tutorial was written by [vike256](https://github.com/vike256/)  
Consider donating: https://github.com/vike256#donations  
Check out [Unibot](https://github.com/vike256/Unibot), my open-source colorbot project  

[Full code here](https://github.com/vike256/tutorials/blob/main/colorbot/main.py)  

## Colorbot

A colorbot is a cheat, usually an aimbot or a triggerbot, that captures the screen and detects enemies based on a specified range of color.  

In this tutorial we'll make an aimbot and a triggerbot.

Before we start we'll have to include the needed libraries
```py
import cv2
import win32api
import win32con
import numpy as np
from time import sleep
from mss import mss
```

Then we define some variables
```py
# Configuration
FOV_X = 256  # FOV width
FOV_Y = 256  # FOV height
SPEED = 1  # Movement speed
UPPER_COLOR = np.array([63, 255, 255])  # Upper bound of the color range to target
LOWER_COLOR = np.array([58, 210, 80])  # Lower bound of the color range to target
```
If you don't know how to find your target color range, see: [Unibot Wiki | Finding target color range](https://github.com/vike256/Unibot/wiki/Finding-target-color-range)


## Mouse input
Mouse input can be done in many ways but we'll use the easiest method: Windows API.
```py
# Defining a function that moves the mouse according to the given x and y value
def mouse_move(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
    print(f'Move {x}, {y}')


# Simulates a left mouse click
def mouse_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    print('Click')
```


## Screen capture
First we have to capture the screen. This can be done in multiple different ways but we will use the library ‘mss’ because it is easy to use.  
To capture screenshots using mss, we need to create a camera object
```py
# Initialize the MSS screenshot capture tool
camera = mss()
```
  
We want to capture a specific area at the center of the screen. Let's get the screen dimensions and define our field of view.
```py
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
```  

Now we can enter our program loop and capture a screenshot. Keep in mind that all code after this is run inside the while loop. Exiting the while loop will end the program.  
```py
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
```

But let's not forget about defining our variables
```py
# Reset variables for each iteration
target = (0, 0)  # Target coordinates
trigger = False  # Flag indicating whether to click
closest_target = None  # Variable to store the closest target contour
```

## Color filtering
The screenshot now looks like this:  
![Game](https://i.imgur.com/6LToF9U.png)

After capturing the screenshot we have to convert it to HSV
```py
# Convert the screenshot to HSV color space for color detection
hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
```  

Then we have to mark what pixels are in our color range
```py
# Create a mask to identify pixels within the specified color range
mask = cv2.inRange(hsv, LOWER_COLOR, UPPER_COLOR)
```  
The mask looks like this:  
![Mask](https://i.imgur.com/nhKy4wJ.png)

After getting the pixels in our color range we need to dilate them to mesh them into a shape for our target
```py
# Apply morphological dilation to increase the size of the detected color blobs
kernel = np.ones((3, 3), np.uint8)
dilated = cv2.dilate(mask, kernel, iterations=5)
```  

Then we convert the image into a binary image
```py
# Apply thresholding to convert the mask into a binary image
thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
```
This is what the thresh looks like:  
![Thresh](https://i.imgur.com/sNJPr3f.png)

Now we just get all the detected targets
```py
# Find contours of the detected color blobs
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
```  

This is an example how the cheat sees the target (Image from [Unibot](https://github.com/vike256/Unibot) debug display):  
![Debug display](https://i.imgur.com/6J7XRTC.png)


## Getting the targets
Now to finish our target detection we have to get the closest target. And get the trigger flag for our triggerbot of course!
```py
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
```




Now we just move our mouse towards the target and click if the target is at the center of the screen
```py
# Calculate the movement values based on the target coordinates
move_x = target[0] * SPEED
move_y = target[1] * SPEED

# Click if target at the center of the screen and left Ctrl is pressed
if trigger and win32api.GetAsyncKeyState(win32con.VK_LCONTROL) < 0:
    mouse_click()

# Move if target outside the center of the screen and right mouse button pressed
if win32api.GetAsyncKeyState(win32con.VK_RBUTTON) < 0 and (move_x != 0 or move_y != 0):
    mouse_move(move_x, move_y)
```
