import threading
import time
import pyautogui
from pynput import keyboard
from pynput import mouse 

RECORD_STATUS = False
REPLAY_STATUS = False

def recordMovements():
    global RECORD_STATUS
    mouse = Controller()
    if(RECORD_STATUS):
        print('The current pointer position is {0}'.format(mouse.position))
        time.sleep(1)
    return 0

def replayMovements():
    global REPLAY_STATUS
    while(REPLAY_STATUS):
        print("Replaying movements")
        time.sleep(1)
    return 0

def on_press(key):
    global RECORD_STATUS
    global REPLAY_STATUS
    record = threading.Thread(target = recordMovements)
    replay = threading.Thread(target = replayMovements)
    
    if key == keyboard.Key.f5 and RECORD_STATUS == False:
        RECORD_STATUS = True
        record.start()
    elif key == keyboard.Key.f5 and RECORD_STATUS == True: 
        RECORD_STATUS = False
    elif key == keyboard.Key.f6 and REPLAY_STATUS == False:
        REPLAY_STATUS = True
        replay.start()
    elif key == keyboard.Key.f6 and REPLAY_STATUS == True:
        REPLAY_STATUS = False

if __name__ == "__main__":
    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
