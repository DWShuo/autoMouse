import threading
import time
import pyautogui
from pynput import keyboard
from pynput import mouse 

RECORD_STATUS = False
REPLAY_STATUS = False

#========MOUSE MOVEMENT RECORD============
def writeData(string):
    f = open("datapoints.txt","a")
    f.write(string)
    f.close()
def on_move(x, y):
    global RECORD_STATUS
    data = '{0}\n'.format((x, y))
    print(data)
    writeData(data)
    if RECORD_STATUS == False:
        return False
def on_click(x, y, button, pressed):
    global RECORD_STATUS
    if(pressed == True):
        data = '{0} {1} {2}'.format(button, pressed ,(x, y))
        print(data)
        writeData(data)
    if RECORD_STATUS == False:
        return False
def recordMovements():
    open('datapoints.txt', 'w').close()#clear the file for new datapoints
    with mouse.Listener( on_move=on_move, on_click=on_click) as listener:
        listener.join()
#=========================================

#========MOUSE MOVEMENT REPLAY============
def replayMovements():
    global REPLAY_STATUS
    with open('datapoints.txt', 'r') as f:
        while REPLAY_STATUS:
            line = f.readline()
            if not line:
                f.seek(0)
            print(line)
    return 0
#=========================================

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
#=========================================

if __name__ == "__main__":
    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
