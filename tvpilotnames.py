# tvpilotnames - setup pilot names to Tiny View Plus by using OSC protocol
# Author: KozakFPV  
# Copyright (C) 2025 by Nobumichi Kozawa

version = "2.0a"

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from pythonosc.udp_client import SimpleUDPClient
import os
import xml.etree.ElementTree as ET
import glob
import subprocess
import threading
import atexit
import time
import pyperclip
import socket

root = Tk()

tvpaddress = StringVar()
labelCamera1 = StringVar()
labelCamera2 = StringVar()
labelCamera3 = StringVar()
labelCamera4 = StringVar()
pnCamera1 = StringVar()
pnCamera2 = StringVar()
pnCamera3 = StringVar()
pnCamera4 = StringVar()

def main():
    global cbC1, cbC2, cbC3, cbC4

    loadIni()
    
    frame = ttk.Frame(root, padding=10)
    fMsg = ttk.Frame(frame, padding=10)
    txtMsg = Text(fMsg, height=15, width=80)

    #loadIni()

    style = ttk.Style()
# comment out following line because 'alt' does not work with MacOS Venture and works with default theme well
    style.theme_use('alt')  # to avoid MacOS Dark mode issue with default ttk thema 'aqua'
    style.configure('TButton', font=('sans-serif', 18))
    style.configure('TLabel', font=('sans-serif', 18))
#    style.configure('TEntry', font=('sans-serif', 18))
    root.title('tvpilotnames')
    frame.pack()

    fTVIp = ttk.Frame(frame)
    fTVIp.pack(anchor=W, pady=2)
    lTVIp = ttk.Label(fTVIp, text=u"Tiny View Plus IP/tvpaddress:")
    lTVIp.pack(side=LEFT)
    eIP1 = ttk.Entry(fTVIp, textvariable=tvpaddress, width=12, font=('sans-serif', 18))
    eIP1.pack(side=LEFT)
    bTVIpLocal = ttk.Button(fTVIp, text="Local", command=bSetLocal)
    bTVIpLocal.pack(side=LEFT)
    
    fC1 = ttk.Frame(frame)
    fC1.pack(anchor=W, pady=2)
    lC1 = ttk.Label(fC1,text=u"カメラ 1  ")
    lC1.pack(side=LEFT)
    eC1Label = ttk.Entry(fC1, textvariable=labelCamera1, width=5, font=('sans-serif', 18))
    eC1Label.pack(side=LEFT)
    cbC1 = ttk.Entry(fC1, state='readonly', textvariable=pnCamera1, width=20, font=('sans-serif', 18))
    cbC1.pack(side=LEFT)
    bCClip1 = ttk.Button(fC1, text=u"クリップボードから送る", width=18, command=bClipSend1)
    bCClip1.pack(side=LEFT)

    fC2 = ttk.Frame(frame)
    fC2.pack(anchor=W, pady=2)
    lC2 = ttk.Label(fC2,text=u"カメラ 2  ")
    lC2.pack(side=LEFT)
    eC2Label = ttk.Entry(fC2, textvariable=labelCamera2, width=5, font=('sans-serif', 18))
    eC2Label.pack(side=LEFT)
    cbC2 = ttk.Entry(fC2, state='readonly', textvariable=pnCamera2, width=20, font=('sans-serif', 18))
    cbC2.pack(side=LEFT)
    bCClip2 = ttk.Button(fC2, text=u"クリップボードから送る", width=18, command=bClipSend2)
    bCClip2.pack(side=LEFT)

    fC3 = ttk.Frame(frame)
    fC3.pack(anchor=W, pady=2)
    lC3 = ttk.Label(fC3,text=u"カメラ 3  ")
    lC3.pack(side=LEFT)
    eC3Label = ttk.Entry(fC3, textvariable=labelCamera3, width=5, font=('sans-serif', 18))
    eC3Label.pack(side=LEFT)
    cbC3 = ttk.Entry(fC3, state='readonly', textvariable=pnCamera3, width=20, font=('sans-serif', 18))
    cbC3.pack(side=LEFT)
    bCClip3 = ttk.Button(fC3, text=u"クリップボードから送る", width=18, command=bClipSend3)
    bCClip3.pack(side=LEFT)


    fC4 = ttk.Frame(frame)
    fC4.pack(anchor=W, pady=2)
    lC4 = ttk.Label(fC4, text=u"カメラ 4  ")
    lC4.pack(side=LEFT)
    eC4Label = ttk.Entry(fC4, textvariable=labelCamera4, width=5, font=('sans-serif', 18))
    eC4Label.pack(side=LEFT)
    cbC4 = ttk.Entry(fC4, state='readonly', textvariable=pnCamera4, width=20, font=('sans-serif', 18))
    cbC4.pack(side=LEFT)
    bCClip4 = ttk.Button(fC4, text=u"クリップボードから送る", width=18, command=bClipSend4)
    bCClip4.pack(side=LEFT)

    fSA = ttk.Frame(frame)
    fSA.pack(expand=1, fill=X)
    lAuthor = ttk.Label(fSA, text="[ V"+str(version)+" by KozakFPV ]")
    lAuthor.pack(side=LEFT)
    bClipSA = ttk.Button(fSA, text=u"クリップボードから全カメラに送る", command=bClipSendAll)
    bClipSA.pack(side=RIGHT)


    root.mainloop()

def bSetLocal():
    tvpaddress.set("127.0.0.1")

def bClipSend1():
    sendPilotName(1)

def bClipSend2():
    sendPilotName(2)

def bClipSend3():
    sendPilotName(3)

def bClipSend4():
    sendPilotName(4)

def bClipSendAll():
    sendPilotName(0)

def checkIpaddress():
    global ipAddress

def disableAll():
    global btnS, btnM, btn1, btn2, cTimeOpt
    btnS["state"] = DISABLED
    btnM["state"] = DISABLED
    btn1["state"] = DISABLED
    btn2["state"] = DISABLED
    cTimeOpt["state"] = DISABLED

def enableAll():
    global btnS, btnM, btn1, btn2, cTimeOpt
    btnS["state"] = NORMAL
    btnM["state"] = NORMAL
    btn1["state"] = NORMAL
    btn2["state"] = NORMAL
    cTimeOpt["state"] = NORMAL

# End of GUI part    

def sendPilotName(camera):
    try:
        ipAddress = socket.gethostbyname(tvpaddress.get())
        print(ipAddress)
        if (ipAddress != ""):
            names = pyperclip.paste().split()
            print("sending...")
            client = SimpleUDPClient(ipAddress, 4000)
            if (0 == camera):
                for c in range(1,5):
                    if (c <= len(names)):
                        oscsend(client, c, names[c-1])
                        time.sleep(0.1)
            else:
                oscsend(client, camera, names[0])
    except:
        messagebox.showinfo("Error", "Tiny View Plus IP address is invalid or not reachable.")

def oscsend(client, camera, pn):
    pn = pn.strip()
    if (pn != ""):
        client.send_message("/v1/camera/"+str(camera)+"/label", pn)
        print("camera"+str(camera)+" / "+pn)
        if (camera == 1):
            pnCamera1.set(pn)
        elif (camera == 2):
            pnCamera2.set(pn)
        elif (camera == 3):
            pnCamera3.set(pn)
        elif (camera == 4):
            pnCamera4.set(pn)


def loadIni():
    global iniFile
    from os.path import expanduser
    home = expanduser("~")
    iniFile = os.path.join(home, 'tvpilotnames.ini')

    try:
        tree = ET.parse(iniFile)
        root = tree.getroot()

        for item in root:
            name = item.attrib["name"]
            value = item.attrib["value"]
            if name == "tvpaddress":
                tvpaddress.set(value)
            if name == "c1":
                labelCamera1.set(value)
            if name == "c2":
                labelCamera2.set(value)
            if name == "c3":
                labelCamera3.set(value)
            if name == "c3":
                labelCamera3.set(value)
    except:
        tvpaddress.set("127.0.0.1")

@atexit.register
def saveIni():
    global iniFile
    root = ET.Element("data")
    item1 = ET.SubElement(root, "item")
    item1.set("name", "tvpaddress")
    item1.set("value", tvpaddress.get())
    item2 = ET.SubElement(root, "item")
    item2.set("name", "c1")
    item2.set("value", labelCamera1.get())
    item3 = ET.SubElement(root, "item")
    item3.set("name", "c2")
    item3.set("value", labelCamera2.get())
    item4 = ET.SubElement(root, "item")
    item4.set("name", "c3")
    item4.set("value", labelCamera3.get())
    item5 = ET.SubElement(root, "item")
    item5.set("name", "c4")
    item5.set("value", labelCamera4.get())
    tree = ET.ElementTree(root)
    tree.write(iniFile, encoding="utf-8")

if __name__ == "__main__":
    main()
