import os
import subprocess
import threading
import time
import traceback

import pyautogui
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import Pyro4

from ip import IP


pyro_process = subprocess.Popen(f'pyro4-ns -n {IP}', shell=False)

    
windows = list(pyautogui.getAllWindows())


poe_found = False


for w in windows:
    if 'Path of Exile' in w.title:
        poe = w
        poe_found = True
        break


if poe_found:
    print('Poe window found')
else:
    print('Poe window NOT found')
    print('Killing Pyro nameserver...')
    os.kill(pyro_process.pid, 1)
    print('Exiting...')
    exit()
    
    
@Pyro4.expose
class Receiver:

    @classmethod
    def catch_event(cls):
        try:
            print('Got event from virtual machine...')
            time.sleep(1)
            print('Switching to desktop')
            pyautogui.hotkey('win', 'd')

            print('Activating POE')
            try:
                poe.activate()
            except:
                pass
            
            time.sleep(0.5)
            print('Pressing enter')
            pyautogui.press('enter')
            
            time.sleep(0.5)
            print('Pasting clipboard')
            pyautogui.hotkey('ctrl', 'v')
            
            print('Pressing enter')
            pyautogui.press('enter')
        except Exception:
            print(traceback.format_exc())


daemon = Pyro4.Daemon(host=IP)  
ns = Pyro4.Proxy(f"PYRO:Pyro.NameServer@{IP}:9090")

Receiver_uri = daemon.register(Receiver)
ns.register('Receiver', Receiver_uri)

print('Pyro listening')

threading.Thread(target=daemon.requestLoop, args=()).start()
