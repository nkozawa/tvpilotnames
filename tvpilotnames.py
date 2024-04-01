# tvpilotnames - setup pilot names to Tiny View Plus by using OSC protocol
# Author: KozakFPV  
# Copyright (C) 2024 by Nobumichi Kozawa

version = "1.0"

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

root = Tk()

ip1 = IntVar()
ip2 = IntVar()
ip3 = IntVar()
ip4 = IntVar()
pilotNamesFile = StringVar()
labelCamera1 = StringVar()
labelCamera2 = StringVar()
labelCamera3 = StringVar()
labelCamera4 = StringVar()
pnCamera1 = StringVar()
pnCamera2 = StringVar()
pnCamera3 = StringVar()
pnCamera4 = StringVar()
pnList = []

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
    root.title('tvpilotnames')
    frame.pack()

    fTVIp = ttk.Frame(frame)
    fTVIp.pack(anchor=W)
    lTVIp = ttk.Label(fTVIp, text=u"Tiny View Plus IP Address:")
    lTVIp.pack(side=LEFT)
    eIP1 = ttk.Entry(fTVIp, textvariable=ip1, width=3)
    eIP1.pack(side=LEFT)
    lIP1 = ttk.Label(fTVIp, text=".")
    lIP1.pack(side=LEFT)
    eIP2 = ttk.Entry(fTVIp, textvariable=ip2, width=3)
    eIP2.pack(side=LEFT)
    lIP2 = ttk.Label(fTVIp, text=".")
    lIP2.pack(side=LEFT)
    eIP3 = ttk.Entry(fTVIp, textvariable=ip3, width=3)
    eIP3.pack(side=LEFT)
    lIP3 = ttk.Label(fTVIp, text=".")
    lIP3.pack(side=LEFT)
    eIP4 = ttk.Entry(fTVIp, textvariable=ip4, width=3)
    eIP4.pack(side=LEFT)
    bTVIpLocal = ttk.Button(fTVIp, text="Local", command=bSetLocal)
    bTVIpLocal.pack(side=LEFT)

    fPN = ttk.Frame(frame)
    fPN.pack(anchor=W, pady=10)
    btnS = ttk.Button(
        fPN, text=u'パイロット名ファイル', width=20,
        command=bPNGetPath)
    btnS.pack(side=LEFT)
    eIN = ttk.Entry(fPN, textvariable=pilotNamesFile, state='readonly', width=31)
    eIN.pack(side=LEFT)
    
    fC1 = ttk.Frame(frame)
    fC1.pack(anchor=W)
    lC1 = ttk.Label(fC1,text=u"カメラ 1  ")
    lC1.pack(side=LEFT)
    eC1Label = ttk.Entry(fC1, textvariable=labelCamera1, width=5)
    eC1Label.pack(side=LEFT)
    cbC1 = ttk.Combobox(fC1, state='readonly', values=pnList, textvariable=pnCamera1, width=30)
    cbC1.pack(side=LEFT)
    bC1 = ttk.Button(fC1, text=u"送る", width=8, command=bSend1)
    bC1.pack(side=LEFT)

    fC2 = ttk.Frame(frame)
    fC2.pack(anchor=W)
    lC2 = ttk.Label(fC2,text=u"カメラ 2  ")
    lC2.pack(side=LEFT)
    eC2Label = ttk.Entry(fC2, textvariable=labelCamera2, width=5)
    eC2Label.pack(side=LEFT)
    cbC2 = ttk.Combobox(fC2, state='readonly', values=pnList, textvariable=pnCamera2, width=30)
    cbC2.pack(side=LEFT)
    bC2 = ttk.Button(fC2, text=u"送る", width=8, command=bSend2)
    bC2.pack(side=LEFT)

    fC3 = ttk.Frame(frame)
    fC3.pack(anchor=W)
    lC3 = ttk.Label(fC3,text=u"カメラ 2  ")
    lC3.pack(side=LEFT)
    eC3Label = ttk.Entry(fC3, textvariable=labelCamera3, width=5)
    eC3Label.pack(side=LEFT)
    cbC3 = ttk.Combobox(fC3, state='readonly', values=pnList, textvariable=pnCamera3, width=30)
    cbC3.pack(side=LEFT)
    bC3 = ttk.Button(fC3, text=u"送る", width=8, command=bSend3)
    bC3.pack(side=LEFT)

    fC4 = ttk.Frame(frame)
    fC4.pack(anchor=W)
    lC4 = ttk.Label(fC4,text=u"カメラ 4  ")
    lC4.pack(side=LEFT)
    eC4Label = ttk.Entry(fC4, textvariable=labelCamera4, width=5)
    eC4Label.pack(side=LEFT)
    cbC4 = ttk.Combobox(fC4, state='readonly',values=pnList, textvariable=pnCamera4, width=30)
    cbC4.pack(side=LEFT)
    bC4 = ttk.Button(fC4, text=u"送る", width=8, command=bSend4)
    bC4.pack(side=LEFT)

    fSA = ttk.Frame(frame)
    fSA.pack(expand=1, fill=X)
    lAuthor = ttk.Label(fSA, text="[ V"+str(version)+" by KozakFPV ]")
    lAuthor.pack(side=LEFT)
    bSA = ttk.Button(fSA, text=u"全カメラに送る", command=bSendAll)
    bSA.pack(side=RIGHT)


    root.mainloop()

def bSetLocal():
    ip1.set(127)
    ip2.set(0)
    ip3.set(0)
    ip4.set(1)

def bPNGetPath():
    pnFile = ""
    pnFile = filedialog.askopenfilename(title="Select Pilot Names File")
    if (pnFile != ""):
        pilotNamesFile.set(pnFile)
        loadPilotNames()
        cbC1["values"] = pnList
        cbC2["values"] = pnList
        cbC3["values"] = pnList
        cbC4["values"] = pnList

def loadPilotNames():
    global pnList
    pnFile = pilotNamesFile.get()
    
    try:
        f = open(pnFile, 'r', encoding='utf-8')
        pnList = f.readlines()
        pnList.insert(0, "N/A")
    except:
        messagebox.showerror("Pilot File", u"パイロットファイルの読み込みに失敗しました")

def bSend1():
    sendPilotName(1)

def bSend2():
    sendPilotName(2)

def bSend3():
    sendPilotName(3)

def bSend4():
    sendPilotName(4)

def bSendAll():
    sendPilotName(0)

def checkIpaddress():
    global ipAddress
    ipAddress = ""
    try:
        i1 = ip1.get()
        i2 = ip2.get()
        i3 = ip3.get()
        i4 = ip4.get()
    except:
        messagebox.showerror("IP Address", u"IP Addressに数値以外の文字が入力されています")
        return

    if (0 <= i1 and i1 < 256 and 0 <= i2 and i2 < 256 and 0<= i3 and i3 < 256 and 0<= i4 and i4 < 256):
        ipAddress = str(i1)+"."+str(i2)+"."+str(i3)+"."+str(i4)
    else:
        messagebox.showerror("IP Address", u"IP Addressに範囲外の数値が指定されています")

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
    checkIpaddress()
    if (ipAddress != ""):
        print("sending...")
        client = SimpleUDPClient(ipAddress, 4000)
        if (0 == camera):
            for c in range(1,5):
                oscsend(client, c)
        else:
            oscsend(client, camera)

def oscsend(client, camera):
    if (1 == camera):
        pn = pnCamera1.get()
    elif (2 == camera):
        pn = pnCamera2.get()
    elif (3 == camera):
        pn = pnCamera3.get()
    elif (4 == camera):
        pn = pnCamera4.get()
    
    if (pn != ""):
        client.send_message("/v1/camera/"+str(camera)+"/label", pn)
        print("camera"+str(camera)+" / "+pn)

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
            if name == "ip1":
                ip1.set(int(value))
            if name == "ip2":
                ip2.set(int(value))
            if name == "ip3":
                ip3.set(int(value))
            if name == "ip4":
                ip4.set(int(value))
            if name == "pnfile":
                pilotNamesFile.set(value)
            if name == "c1":
                labelCamera1.set(value)
            if name == "c2":
                labelCamera2.set(value)
            if name == "c3":
                labelCamera3.set(value)
            if name == "c3":
                labelCamera3.set(value)

        loadPilotNames()
    except:
        ip1.set(127)
        ip2.set(0)
        ip3.set(0)
        ip4.set(1)
        pilotNamesFile.set("")

@atexit.register
def saveIni():
    global iniFile
    root = ET.Element("data")
    item1 = ET.SubElement(root, "item")
    item1.set("name", "ip1")
    try:
        item1.set("value", str(ip1.get()))
    except:
        item1.set("value", "0")
    item2 = ET.SubElement(root, "item")
    item2.set("name", "ip2")
    try:
        item2.set("value", str(ip2.get()))
    except:
        item2.set("value", "0")
    item3 = ET.SubElement(root, "item")
    item3.set("name", "ip3")
    try:
        item3.set("value", str(ip3.get()))
    except:
        item3.set("value", "0")
    item4 = ET.SubElement(root, "item")
    item4.set("name", "ip4")
    try:
        item4.set("value", str(ip4.get()))
    except:
        item4.set("value", "0")

    item5 = ET.SubElement(root, "item")
    item5.set("name", "pnfile")
    item5.set("value", pilotNamesFile.get())
    item6 = ET.SubElement(root, "item")
    item6.set("name", "c1")
    item6.set("value", labelCamera1.get())
    item7 = ET.SubElement(root, "item")
    item7.set("name", "c2")
    item7.set("value", labelCamera2.get())
    item8 = ET.SubElement(root, "item")
    item8.set("name", "c3")
    item8.set("value", labelCamera3.get())
    item9 = ET.SubElement(root, "item")
    item9.set("name", "c4")
    item9.set("value", labelCamera4.get())
    tree = ET.ElementTree(root)
    tree.write(iniFile, encoding="utf-8")

if __name__ == "__main__":
    main()
