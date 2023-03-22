from win32api import keybd_event
from win32con import KEYEVENTF_KEYUP, VK_VOLUME_UP, VK_VOLUME_DOWN
from time import sleep

def increase_volume():
    keybd_event(VK_VOLUME_UP, 0)
    keybd_event(VK_VOLUME_UP, 0, KEYEVENTF_KEYUP)

def decrease_volume():
    keybd_event(VK_VOLUME_DOWN, 0)
    keybd_event(VK_VOLUME_DOWN, 0, KEYEVENTF_KEYUP)

def keepWindowAlive():
    while True:
        increase_volume()
        sleep(1)
        decrease_volume()
        sleep(300)
