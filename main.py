import serial
import time
import os.path
from datetime import datetime
import serial.tools.list_ports
import tkinter.messagebox as mb
import tkinter as tk





ports = serial.tools.list_ports.comports()
if len(ports) > 1:
    sel_com = tk.Tk()
    buttons = [tk.Button(sel_com, text=p.name) for p in ports]
    for b in buttons:
        b.pack()
    sel_com.mainloop()



for p in ports:
    print(p)

def add_cards():
    port = "COM3"
    baudrate = 9600
    # seri = serial.Serial()
    # seri.tru

    try:
        ser = serial.Serial(port, baudrate=baudrate)
    except serial.serialutil.SerialException:
        mb.showwarning(" Com port busy")
    ser.write(b"\x35\x07\x00\x00\x00\x72\x8F")
    data_r = ser.read(10)
    print(data_r)
    ser.close()
    # time.sleep(1)
    #ser.flushinput()
    with serial.Serial(port, baudrate=baudrate) as ser:
        while True:
            ser.write(b"\x05\x07\x00\x00\x00\x32\x8B")
            data_r = ser.read(16)
            #print (data_r)
            if data_r == b'\x05\x10\x00\x00\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x1dZ':
                time.sleep(0.1)
                continue
            d = ""
            for ch in data_r[8:9]:
                d += str(int(ch))
            #print(d+",", end="")
            strW =str(d)+","+str(int("0x"+((data_r[7:5:-1]).hex()),0))
            strU = int("0x"+((data_r[8:5:-1]).hex()),0)
            print(strW)
            print(strU)
            if not os.path.isfile("cards.csv"):
                with open("cards.csv", "w") as fcsv:
                    fcsv.write("sep=;\n")
                    fcsv.write("<b>WIEGAND</b>;УНИВЕРСАЛЬНЫЙ;ДАТА;ВРЕМЯ\n")

            with open("cards.csv", "a") as fcsv:
                date_time = str(datetime.now())
                cur_date = date_time.split()[0]
                cur_time = date_time.split()[1]
                cur_time = cur_time.split('.')[0]

                fcsv.write(str(strW)+";"+str(strU)+";"+cur_date+";"+cur_time+"\n")
            #print(data_r[6:9])
            #print(int(chr(data_r[8:9])))
            time.sleep(0.5)


# fhand = open("getlic.txt", "r")
# ftext = fhand.read()
# crypttext=''
# for chr in ftext:
# 	crypttext += str(ord(chr))
# 	crypttext +=str(ord('!'))
# 	crypttext +=str(ord('*'))
# 	crypttext +=str(ord('&'))
# #message(ord('!'))
# #message(ord('*'))
# #message(ord('&'))
# fhand.close()
# fhand = open("Rename.lic", "w")
# fhand.write(crypttext)
# fhand.close()






 #   \x35\x0A\x00\x00\x00\x00\x4E\x03\xE3\x75