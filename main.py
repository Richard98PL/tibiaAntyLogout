from pynput.keyboard import Key, Controller
import win32gui
import win32con
import re
import time
import datetime
from random import randint
keyboard = Controller()

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

    def get_rectangle(self):
        win32gui.GetWindowRect(self._handle)

def antyLogout():
    currentWindowManager = WindowMgr()
    currentWindow = win32gui.GetForegroundWindow()
    currentWindowManager._handle = currentWindow

    tibiaWindowManager = WindowMgr()
    tibiaWindowManager.find_window_wildcard(".*Tibia.*")
    
    if currentWindowManager._handle != tibiaWindowManager._handle:
        win32gui.ShowWindow(tibiaWindowManager._handle, win32con.SW_MAXIMIZE)
        tibiaWindowManager.set_foreground()

    keyboard.press(Key.ctrl)
    movementKeys = [Key.up, Key.down]
    for key in movementKeys:
        keyboard.tap(key)
        time.sleep( randint(15,31) / 1000)
    keyboard.release(Key.ctrl)

    now = datetime.datetime.now()
    print(now.hour, now.minute, now.second)

    if currentWindowManager._handle != tibiaWindowManager._handle:
        win32gui.ShowWindow(tibiaWindowManager._handle, win32con.SW_MINIMIZE)
        currentWindowManager.set_foreground()
    
antyLogout()
while True:
    time.sleep(6*60 + randint(0,13))
    antyLogout()
