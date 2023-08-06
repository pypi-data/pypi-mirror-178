import os, ctypes, sys
from colorama import init, Fore as color
from time import sleep as _sleep, strftime, time, gmtime
init()

class consoler:
    def __init__(self):
        self.type = 'nt'
        self.kernel32 = ctypes.WinDLL('kernel32')
        self.user32 = ctypes.WinDLL('user32')
        self.hide = 0
        self.unhide = 1
        self.start_time = 0
        self.MB_OK = 0x0
        self.MB_OKCXL = 0x01
        self.MB_YESNOCXL = 0x03
        self.MB_YESNO = 0x04
        self.MB_HELP = 0x4000
        self.ICON_EXCLAIM = 0x30
        self.ICON_INFO = 0x40
        self.ICON_STOP = 0x10

    def size(self, x:int=None, y:int=None):
        if x is None:
            return
        elif y is None:
            return
        else:
            if os.name == self.type:
                os.system('mode {},{}'.format(x, y))

    def clear(self):
        if os.name == self.type:
            os.system('cls')
        else:
            os.system('clear')

    def hideconsole(self):
        window = self.kernel32.GetConsoleWindow()
        if window:
            self.user32.ShowWindow(window, self.hide)

    def unhideconsole(self):
        window = self.kernel32.GetConsoleWindow()
        if window:
            self.user32.ShowWindow(window, self.unhide)
    
    def set_title(self, title: str=None):
        if title is None:
            return
        else:
            if sys.version[0] == 3:
                return ctypes.windll.kernel32.SetConsoleTitleW(title)
            elif sys.version[0] == 2:
                return ctypes.windll.kernel32.SetConsoleTitleA(title)
            else:
                return ctypes.windll.kernel32.SetConsoleTitleW(title)
    
    def sleep(self, timer: int=None):
        if timer is None:
            return
        else:
            return _sleep(secs=timer)

    def typeprint(self, str, velo: int=None):
        if velo is None:
            velo = 0.1 
        else:
            velo = velo

        for letter in str:
            sys.stdout.write(letter)
            sys.stdout.flush()
            _sleep(0.1)
    
    def savelogs(self, text: str=None, path: str=None, printerror=False, type: str=None):
        if type is None:
            type = 'a'
        elif type == 'read':
            type = 'r'
        elif type == 'write':
            type = 'w'
        else:
            type = 'a'

        try:
            data_file = open(f'{path}.log', type).writelines(text)
        except Exception as e:
            if printerror is True:
                print(f'{color.RED}{e}')
    
    def messagebox(self, title: str=None, message: str=None):
        if sys.version[0] == 3:
            result = ctypes.windll.user32.MessageBoxW(0, message, title)
        elif sys.version[0] == 2:
            result = ctypes.windll.user32.MessageBoxW(0, message, title)
        else:
            result = ctypes.windll.user32.MessageBoxW(0, message, title)