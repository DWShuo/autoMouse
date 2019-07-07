import threading
import time
import pyautogui
from pynput import keyboard
from pynput import mouse 

RECORD_STATUS = False
REPLAY_STATUS = False
pyautogui.FAILSAFE = False
MOVE_TIMER = -1
#========MOUSE MOVEMENT RECORD============
def writeData(string):
    f = open("datapoints.txt","a")
    f.write(string)
    f.close()
def on_move(x, y):
    global MOVE_TIMER
    global RECORD_STATUS
    temp_time = time.time_ns()
    time_elapsed = (temp_time - MOVE_TIMER)/1000000000
    MOVE_TIMER = temp_time
    data = '{0} {1} {2}\n'.format(x, y, time_elapsed)
    print(data)
    writeData(data)
    if RECORD_STATUS == False:
        return False
def on_click(x, y, button, pressed):
    global MOVE_TIMER
    global RECORD_STATUS
    if(pressed == True):
        temp_time = time.time_ns()
        time_elapsed = (temp_time - MOVE_TIMER)/1000000000
        MOVE_TIMER = temp_time
        data = '{0} {1} {2} {3}\n'.format(button,x, y, time_elapsed)
        print(data)
        writeData(data)
    if RECORD_STATUS == False:
        return False
def recordMovements():
    global MOVE_TIMER
    MOVE_TIMER = time.time_ns()
    open('datapoints.txt', 'w').close()#clear the file for new datapoints
    with mouse.Listener( on_move=on_move, on_click=on_click) as listener:
        listener.join()
#=========================================

#========MOUSE MOVEMENT REPLAY============
def replayMovements():
    global REPLAY_STATUS
    mouseControl = mouse.Controller()
    with open('datapoints.txt', 'r') as f:
        while REPLAY_STATUS:
            line = f.readline()
            if not line:#EOF move to top of datapoints
                f.seek(0)
                line = f.readline()#re-read line
            data = line.split()
            if len(data) == 3:
                mouseControl.position = ( int(data[0]) ,int(data[1]) )
                time.sleep(float(data[2]))
                #pyautogui.moveTo(int(data[0]),int(data[1]), 0.01)#pyautogui mouse movment too slow
            elif len(data) == 4:
                data[0] = data[0].split('.')[1]
                pyautogui.click(button = data[0],x = int(data[1]), y = int(data[2]))
                time.sleep(float(data[3]))
            else:
                print("invalid datapoint format")
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
