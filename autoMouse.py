import threading
import time
import pyautogui
from pynput import keyboard
from pynput import mouse 

RECORD_STATUS = False
REPLAY_STATUS = False
#========MOUSE MOVEMENT RECORD============
def on_move(x, y):
    global RECORD_STATUS
    print('Pointer moved to {0}'.format(
        (x, y)))
    if RECORD_STATUS == False:
        return False
def on_click(x, y, button, pressed):
    global RECORD_STATUS
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if RECORD_STATUS == False:
        return False
def recordMovements():
    with mouse.Listener( on_move=on_move, on_click=on_click) as listener:
        listener.join()
#========MOUSE MOVEMENT RECORD============

#========MOUSE MOVEMENT REPLAY============
def replayMovements():
    global REPLAY_STATUS
    while(REPLAY_STATUS):
        print("Replaying movements")
        time.sleep(1)
    return 0
#========MOUSE MOVEMENT REPLAY============

#========HOTKEY COMMAND LISTEN============
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
#========HOTKEY COMMAND LISTEN============

if __name__ == "__main__":
    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
