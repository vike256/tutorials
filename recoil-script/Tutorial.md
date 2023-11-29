This tutorial was written by [vike256](https://github.com/vike256/)  
Consider donating: https://github.com/vike256#donations  
Check out [Unibot](https://github.com/vike256/Unibot), my open-source colorbot project  

## Recoil script
A recoil script is a program that automatically adjusts the mouse position to counteract the recoil of a weapon in a video game.  

Python is a popular language for writing recoil scripts because it is easy to learn and use. It also has a number of libraries that can be used to interact with the Windows API, which is necessary for controlling the mouse.

## Importing libraries
To write a recoil script in Python, you will need to import the following libraries:
```py
import win32api  # Import the win32api library to interact with the Windows API
import win32con  # Import the win32con library for Windows constants
import time  # Import the time library for timing operations
```

If you don't have the win32api library installed you can install it with this console command:  
```
pip install pywin32
```

## Configuring settings
Before you can write the recoil script, you need to configure some settings. These settings will determine how much the mouse moves each time the script is executed.
```py
# Define constants for recoil values and delay
RECOIL_X = 0  # Horizontal recoil value
RECOIL_Y = 10  # Vertical recoil value
DELAY = 10  # Delay in milliseconds between adjustments
```
The DELAY constant specifies how long the script should wait between each recoil adjustment. This is important because you don't want the script to run too fast or inconsistantly.

## Mouse input
Define a function for mouse movement. We'll use Windows API for this.
```py
# Defining a function that moves the mouse according to the given x and y value
def mouse_move(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
    print(f'Move {x}, {y}')
```

## Writing the script
The main part of the recoil script is a loop that checks for mouse input. When the left mouse button is down, the script moves the mouse to counteract the recoil.
```py
def main():
    print('Start')
    # The main program loop
    while True:
        # Check if the F1 key is pressed to exit the loop
        if win32api.GetAsyncKeyState(win32con.VK_F1) < 0:
            break

        # Check if the left mouse button is clicked to trigger recoil adjustment
        if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0:
            mouse_move(RECOIL_X, RECOIL_Y)  # Send mouse input based on recoil values

        time.sleep(DELAY / 1000)  # Delay between adjustments

    print('Exit')


# Run the main program
if __name__ == '__main__':
    main()
```

The mouse_move function takes two arguments: x and y. The x argument specifies how much the mouse should move horizontally, and the y argument specifies how much the mouse should move vertically.

The time.sleep function pauses the script for a specified amount of time. In this case, the script pauses for DELAY / 1000 milliseconds, which is equal to DELAY divided by 1000. This means that the script will wait for DELAY milliseconds before moving the mouse again.
