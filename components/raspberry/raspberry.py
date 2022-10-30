import subprocess 
import sys
import os, signal

from pathlib import Path

process = None
#processId = None

def start():
    global process
    #global processId

    arg = [str(Path.home())+'/qemu-system-aarch64', '-m', '1024', '-M', 'raspi3', '-kernel', 
    str(Path.home())+'/kernel8.img', '-dtb', str(Path.home())+'/bcm2710-rpi-3-b-plus.dtb', '-sd',  
    str(Path.home())+'/2020-08-20-raspios-buster-armhf.img', '-append', 
    'console=ttyAMA0 root=/dev/mmcblk0p2 rw rootwait rootfstype=ext4', '-nographic',
    '-device', 'usb-net,netdev=net0', '-netdev', 'user,id=net0,hostfwd=tcp::5555-:22']

    process = subprocess.Popen(arg, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
  

def stop(): 
    process.kill()

def read(arg_term, arg_module, arg_graphics):
    pass
    
def write():
    return True

