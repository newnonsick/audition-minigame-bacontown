import os
import warnings
import keyboard
import time
import numpy as np
import pyautogui
import win32gui
import cv2
import pygetwindow as gw
import requests

# def draw_roi():
#     global window_title
#     window = gw.getWindowsWithTitle(window_title)[0]
#     if window is None:
#         return
#     # left, top, right, bottom = window.left, window.top, window.left + window.width, window.top + window.height
#     # window.left + 795, window.top + 850, window.left + window.width - 795, window.top + window.height - 185
#     #1 window.left + 795, window.top + 850, window.left + window.width - 1080, window.top + window.height - 185
#     #2 window.left + 842, window.top + 850, window.left + window.width - 1031, window.top + window.height - 185
#     #3 window.left + 889, window.top + 850, window.left + window.width - 984, window.top + window.height - 185
#     #4 window.left + 936, window.top + 850, window.left + window.width - 937, window.top + window.height - 185
#     #5 window.left + 983, window.top + 850, window.left + window.width - 890, window.top + window.height - 185
#     #6 window.left + 1030, window.top + 850, window.left + window.width - 843, window.top + window.height - 185
#     #7 window.left + 1077, window.top + 850, window.left + window.width - 796, window.top + window.height - 185
#     #space window.left + 1050, window.top + 820, window.left + window.width - 830, window.top + window.height - 240

#     # left, top, right, bottom = window.left, window.top, window.left + window.width, window.top + window.height
#     # window.left + 795, window.top + 850, window.left + window.width - 795, window.top + window.height - 185
#     #1 window.left + 820, window.top + 850, window.left + window.width - 1055, window.top + window.height - 185
#     #2 window.left + 867, window.top + 850, window.left + window.width - 1006, window.top + window.height - 185
#     #3 window.left + 914, window.top + 850, window.left + window.width - 959, window.top + window.height - 185
#     #4 window.left + 961, window.top + 850, window.left + window.width - 912, window.top + window.height - 185
#     #5 window.left + 1008, window.top + 850, window.left + window.width - 865, window.top + window.height - 185
#     #6 window.left + 1055, window.top + 850, window.left + window.width - 818, window.top + window.height - 185
#     #space window.left + 1025, window.top + 820, window.left + window.width - 855, window.top + window.height - 240
#     left, top, right, bottom = window.left + 1055, window.top + 850, window.left + window.width - 818, window.top + window.height - 185
#     screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
#     screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
#     cv2.rectangle(screenshot, (0, 0), (right - left, bottom - top), (0, 255, 0), 2)
#     cv2.imshow(f'{window.width} {window.height}', screenshot)
#     cv2.waitKey(1)

# def update_window_position():
#     global window_positions
#     global window_title
#     while True:
#         window = gw.getWindowsWithTitle(window_title)[0]
#         if window is not None:
#             window_positions = []
#         window_positions = [
#             [window.left + 795, window.top + 850, window.left + window.width - 1080, window.top + window.height - 185],
#             [window.left + 842, window.top + 850, window.left + window.width - 1031, window.top + window.height - 185],
#             [window.left + 889, window.top + 850, window.left + window.width - 984, window.top + window.height - 185],
#             [window.left + 936, window.top + 850, window.left + window.width - 937, window.top + window.height - 185],
#             [window.left + 983, window.top + 850, window.left + window.width - 890, window.top + window.height - 185],
#             [window.left + 1030, window.top + 850, window.left + window.width - 843, window.top + window.height - 185],
#             [window.left + 1077, window.top + 850, window.left + window.width - 796, window.top + window.height - 185]
#         ]
#         time.sleep(1)

def press_key(key):
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)


def looking_for_press_space():
    global window_index
    global window_title
    global space_position
    while True:
        window = gw.getWindowsWithTitle(window_title)[0]
        if window is not None:
            left, top, right, bottom = space_position
            screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
            location = pyautogui.locate('D://fishtest//dot.png', screenshot, confidence=0.8)
            if location:
                press_key('space')
                window_index = 0
                break

def looking_for_press_key():
  
    while True:
        global image_paths
        global window_positions
        global window_index

        left, top, right, bottom = window_positions[window_index]
        screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
        for image_path in image_paths:
            location = pyautogui.locate(image_path, screenshot, confidence=0.9)
            if location:
                if 'left' in image_path:
                    if 'blue' in image_path:
                        press_key('left')
                    else:
                        press_key('right')
                elif 'right' in image_path:
                    if 'blue' in image_path:
                        press_key('right')
                    else:
                        press_key('left')
                elif 'up' in image_path:
                    if 'blue' in image_path:
                        press_key('up')
                    else:
                        press_key('down')
                elif 'down' in image_path:
                    if 'blue' in image_path:
                        press_key('down')
                    else:
                        press_key('up')
                
                window_index += 1
                if window_index >= len(window_positions):
                    window_index = 0
                    looking_for_press_space()
                #looking_for_press_key()
                break

def printStatus():
    os.system('cls')
    text = """
     _         _        _____ _     _     _             
    / \  _   _| |_ ___ |  ___(_)___| |__ (_)_ __   __ _ 
   / _ \| | | | __/ _ \| |_  | / __| '_ \| | '_ \ / _` |
  / ___ \ |_| | || (_) |  _| | \__ \ | | | | | | | (_| |
 /_/   \_\__,_|\__\___/|_|   |_|___/_| |_|_|_| |_|\__, |
                                                  |___/                                                  
"""
    print(text)
    print("  Working with the FiveM® by Cfx.re - Bacon Town. Resolution: 1920x1080 windowed")


def printOutdated():
    os.system('cls')
    text = """
     _         _        _____ _     _     _             
    / \  _   _| |_ ___ |  ___(_)___| |__ (_)_ __   __ _ 
   / _ \| | | | __/ _ \| |_  | / __| '_ \| | '_ \ / _` |
  / ___ \ |_| | || (_) |  _| | \__ \ | | | | | | | (_| |
 /_/   \_\__,_|\__\___/|_|   |_|___/_| |_|_|_| |_|\__, |
                                                  |___/                                              
"""
    print(text)
    print("  Your version of the program is outdated. Please download the latest version.")
    print("  Link: https://drive.google.com/file/d/1xS8DZ0VekeRzM0YKBpvYWpGidZxQ1vBB/view?usp=sharing")
    print("  Press any key to exit the program.")
    url = 'https://drive.google.com/file/d/1xS8DZ0VekeRzM0YKBpvYWpGidZxQ1vBB/view?usp=sharing'
    os.system(f'start {url}')
    keyboard.read_key()
    os._exit(0)

def printFiveMNotFound():
    os.system('cls')
    text = """
     _         _        _____ _     _     _             
    / \  _   _| |_ ___ |  ___(_)___| |__ (_)_ __   __ _ 
   / _ \| | | | __/ _ \| |_  | / __| '_ \| | '_ \ / _` |
  / ___ \ |_| | || (_) |  _| | \__ \ | | | | | | | (_| |
 /_/   \_\__,_|\__\___/|_|   |_|___/_| |_|_|_| |_|\__, |
                                                  |___/                                              
"""
    print(text)
    print("  FiveM® by Cfx.re - Bacon Town not found. Please open the game.")
    print("  Retrying in 1 second...")
    time.sleep(1)

def checkVersion():
    try:
        response = requests.get('https://pastebin.com/raw/012zh2qx', verify=False)
        latest_version = response.text.strip()
        current_version = '1.0.0'
        if latest_version != current_version:
            printOutdated()
    except Exception as e:
        os.system('cls')
        print("Error checking the version:", e)
        keyboard.read_key()
        os._exit(0)

def find_window(title):
        hwnd = win32gui.FindWindow(None, title)
        if hwnd:
            return hwnd
        else:
            raise Exception(f"Window with title '{title}' not found")

def checkGameAppear():
    while True:
        try:
            hwnd = find_window(window_title)
            time.sleep(1)
            return hwnd
            break
        except Exception as e:
            printFiveMNotFound()


if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    checkVersion()
    
    window_positions = []
    window_index = 0

    image_folder = fr'D:\fishtest\image'
    image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith('.png')]

    window_title = "FiveM® by Cfx.re - Bacon Town"
    # window_title = "Screenshot 2024-06-09 161100.png ‎- Photos"

    hwnd = checkGameAppear()
    
    printStatus()

    #select option
    while True:
        print("  Select the option:")
        print("  [1] - Shallow water fishing")
        print("  [2] - Deep sea fishing")
        option = input("  Option: ")
        if option not in ['1', '2']:
            print("  Invalid option. Please select a valid option.")
            keyboard.read_key()
            os.system('cls')
            printStatus()
        else:
            break

    win32gui.SetForegroundWindow(hwnd)
    

    window = gw.getWindowsWithTitle(window_title)[0]

    if window is not None:
        window_positions = []

    if option == '1':
        window_positions = [
        [window.left + 820, window.top + 850, window.left + window.width - 1055, window.top + window.height - 185],
        [window.left + 867, window.top + 850, window.left + window.width - 1006, window.top + window.height - 185],
        [window.left + 914, window.top + 850, window.left + window.width - 959, window.top + window.height - 185],
        [window.left + 961, window.top + 850, window.left + window.width - 912, window.top + window.height - 185],
        [window.left + 1008, window.top + 850, window.left + window.width - 865, window.top + window.height - 185],
        [window.left + 1055, window.top + 850, window.left + window.width - 818, window.top + window.height - 185]
        ]
        space_position = [window.left + 1025, window.top + 820, window.left + window.width - 855, window.top + window.height - 240]
    elif option == '2':
        window_positions = [
        [window.left + 795, window.top + 850, window.left + window.width - 1080, window.top + window.height - 185],
        [window.left + 842, window.top + 850, window.left + window.width - 1031, window.top + window.height - 185],
        [window.left + 889, window.top + 850, window.left + window.width - 984, window.top + window.height - 185],
        [window.left + 936, window.top + 850, window.left + window.width - 937, window.top + window.height - 185],
        [window.left + 983, window.top + 850, window.left + window.width - 890, window.top + window.height - 185],
        [window.left + 1030, window.top + 850, window.left + window.width - 843, window.top + window.height - 185],
        [window.left + 1077, window.top + 850, window.left + window.width - 796, window.top + window.height - 185]
        ]
        space_position = [window.left + 1050, window.top + 820, window.left + window.width - 830, window.top + window.height - 240]
        
    

    looking_for_press_key()



