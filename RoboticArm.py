#!/usr/bin/python2
################################################################################
# Author:   James Cribb (cribb-it.co.uk)
# Date:     21-Dec-2016
# Props:    http://www.wikihow.com/Use-a-USB-Robotic-Arm-with-a-Raspberry-Pi-%28Maplin%29
# Props:    https://walac.github.io/pyusb/
# Requires: PyUSB and Tkinker to be installed.
#           PyUSB requires a USB lib please go the PyUSB web for more details
# Decription:
#    This is a python script that connect to the Maplin (A37JN) \
#    Velleman KSR10 USB robotic arm and displays a simple GUI to
#    control it.
################################################################################

# Import the USB and Time librarys into Python
import usb.core, usb.util#, usb.backend.libusb1
import time
import tkFileDialog, tkMessageBox
import math
import os
from Tkinter import *
# Height and Width for Buttons
btnX = 2
btnY = 10

class App:
    
    def __init__(self, master):
        
        # State Veritables
        self.light = 0
        self.rec = 0
        self.ticks = 0
        self.cmd = [0,0,0]
        
        master.title("USB Robotic Arm")
        
        master.bind("<KeyPress-i>", self.baseLeft)
        master.bind("<KeyPress-k>", self.baseRight)
        master.bind("<KeyPress-u>", self.shoulderUp)
        master.bind("<KeyPress-j>", self.shoulderDown)
        master.bind("<KeyPress-r>", self.elbowUp)
        master.bind("<KeyPress-f>", self.elbowDown)
        master.bind("<KeyPress-e>", self.wristUp)
        master.bind("<KeyPress-d>", self.wristDown)
        master.bind("<KeyPress-w>", self.handOpen)
        master.bind("<KeyPress-s>", self.handClose)
        master.bind("<KeyPress-l>", self.ledOnOFF)
        master.bind("<KeyRelease>", self.buttonRelease)
        
        menubar = Menu(master)
        # create a file menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.askopenfilename)
        filemenu.add_command(label="Save", command=self.asksaveasfilename)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        # create more pulldown menus
        #editmenu = Menu(menubar, tearoff=0)
        #editmenu.add_command(label="Cut")
        #editmenu.add_command(label="Copy")
        #editmenu.add_command(label="Paste")
        #menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)  
        # Add the menubar to the main appliction
        master.config(menu=menubar)
        # Setting for file dialogs
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt'), ('dat files', '.dat')]
        options['initialdir'] = '~'
        options['initialfile'] = 'robotic_arm.txt'
        options['parent'] = master
        options['title'] = 'Robot Command File'
        
        #frame = Frame(master, height=320, width=320, bg="DarkGrey")
        #frame.pack_propagate(0) # don't shrink
        #frame.pack()
        
        groupBase = LabelFrame(master, text="Base", padx=5, pady=5)
        groupBase.grid(padx=10, pady=5, row=1, column=1)

        self.baseButtonLeft = Button(groupBase, text="Left", height=btnX, width=btnY) #command=self.stopArm
        self.baseButtonLeft.bind("<Button-1>", self.baseLeft)
        self.baseButtonLeft.bind("<ButtonRelease-1>", self.buttonRelease)
        self.baseButtonLeft.pack(side=LEFT, expand=1)
        
        self.baseButtonRight = Button(groupBase, text="Right", height=btnX, width=btnY)
        self.baseButtonRight.bind("<Button-1>", self.baseRight)
        self.baseButtonRight.bind("<ButtonRelease-1>", self.buttonRelease)
        self.baseButtonRight.pack(side=LEFT, expand=1)
        
        groupShoulder = LabelFrame(master, text="Shoulder", padx=5, pady=5)
        groupShoulder.grid(padx=10, pady=5, row=2, column=1)

        self.shoulderButtonUp = Button(groupShoulder, text="Up", height=btnX, width=btnY)
        self.shoulderButtonUp.bind("<Button-1>", self.shoulderUp)
        self.shoulderButtonUp.bind("<ButtonRelease-1>", self.buttonRelease)
        self.shoulderButtonUp.pack(side=LEFT, expand=1)
        
        self.shoulderButtonDown = Button(groupShoulder, text="Down", height=btnX, width=btnY)
        self.shoulderButtonDown.bind("<Button-1>", self.shoulderDown)
        self.shoulderButtonDown.bind("<ButtonRelease-1>", self.buttonRelease)
        self.shoulderButtonDown.pack(side=LEFT, expand=1)
        
        groupElbow = LabelFrame(master, text="Elbow", padx=5, pady=5)
        groupElbow.grid(padx=10, pady=5, row=3, column=1)

        self.elbowButtonUp = Button(groupElbow, text="Up", height=btnX, width=btnY)
        self.elbowButtonUp.bind("<Button-1>", self.elbowUp)
        self.elbowButtonUp.bind("<ButtonRelease-1>", self.buttonRelease)
        self.elbowButtonUp.pack(side=LEFT, expand=1)
        
        self.elbowButtonDown = Button(groupElbow, text="Down", height=btnX, width=btnY)
        self.elbowButtonDown.bind("<Button-1>", self.elbowDown)
        self.elbowButtonDown.bind("<ButtonRelease-1>", self.buttonRelease)
        self.elbowButtonDown.pack(side=LEFT, expand=1)
        
        groupWrist = LabelFrame(master, text="Wrist", padx=5, pady=5)
        groupWrist.grid(padx=10, pady=5, row=4, column=1)

        self.wristButtonUp = Button(groupWrist, text="Up", height=btnX, width=btnY)
        self.wristButtonUp.bind("<Button-1>", self.wristUp)
        self.wristButtonUp.bind("<ButtonRelease-1>", self.buttonRelease)
        self.wristButtonUp.pack(side=LEFT, expand=1)
        
        self.wristButtonDown = Button(groupWrist, text="Down", height=btnX, width=btnY)
        self.wristButtonDown.bind("<Button-1>", self.wristDown)
        self.wristButtonDown.bind("<ButtonRelease-1>", self.buttonRelease)
        self.wristButtonDown.pack(side=LEFT, expand=1)
        
        groupGrip = LabelFrame(master, text="Hand/Gripper", padx=5, pady=5)
        groupGrip.grid(padx=10, pady=5, row=5, column=1)

        self.handButtonOpen = Button(groupGrip, text="Open", height=btnX, width=btnY)
        self.handButtonOpen.bind("<Button-1>", self.handOpen)
        self.handButtonOpen.bind("<ButtonRelease-1>", self.buttonRelease)
        self.handButtonOpen.pack(side=LEFT, expand=1)
        
        self.handButtonClose = Button(groupGrip, text="Close", height=btnX, width=btnY)
        self.handButtonClose.bind("<Button-1>", self.handClose)
        self.handButtonClose.bind("<ButtonRelease-1>", self.buttonRelease)
        self.handButtonClose.pack(side=LEFT, expand=1)
        
        groupLED = LabelFrame(master, text="Light", padx=5, pady=5)
        groupLED.grid(padx=10, pady=5, row=6, column=1)

        self.ledButtonOn = Button(groupLED, text="On", height=btnX, width=btnY, command=self.ledOn)
        self.ledButtonOn.pack(side=LEFT, expand=1)
        
        self.ledButtonOff = Button(groupLED, text="Off", height=btnX, width=btnY, command=self.ledOff)
        self.ledButtonOff.pack(side=LEFT, expand=1)
           
        groupRec = LabelFrame(master, text="Record", padx=5, pady=5)
        groupRec.grid(padx=10, pady=5, row=1, column=2)

        self.recButtonOn = Button(groupRec, text="Record", height=btnX, width=btnY, command=self.record)
        self.recButtonOn.pack(side=LEFT, expand=1)
        
        self.recButtonOff = Button(groupRec, text="Pause", height=btnX, width=btnY, state=DISABLED, command=self.pause)
        self.recButtonOff.pack(side=LEFT, expand=1)

        self.recButtonPlay = Button(groupRec, text="Play", height=btnX, width=btnY, command=self.play)
        self.recButtonPlay.pack(side=LEFT, expand=1)
        
        self.recButtonClear = Button(groupRec, text="Clear", height=btnX, width=btnY, command=self.clear)
        self.recButtonClear.pack(side=LEFT, expand=1)
        
        self.listbox = Listbox(master)
        self.listbox.grid(row=2, column=2,rowspan=5, sticky=W+E+N+S, padx=10, pady=10)
        #self.listbox.insert(END, "0:[0,0,1]")

        self.status = Canvas(master, width=175, height=25)
        self.status.grid(row=7, column=1, columnspan=2, sticky=E)
        self.status.create_text(55, 15, text="Battery Status:")
        self.g = self.status.create_rectangle(105, 5, 120, 25)
        self.y = self.status.create_rectangle(120, 5, 135, 25)
        self.o = self.status.create_rectangle(135, 5, 150, 25)
        self.r = self.status.create_rectangle(150, 5, 165, 25)

    def sendCmd(self, ArmCmd):
        self.ticks = time.time()
        result = RobotArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,3)
        #self.setStatus(result)
        #print('Send Cmd = ', ArmCmd)   
        
    def baseLeft(self, event):        
        self.cmd = [0,1,self.light]
        self.sendCmd(self.cmd)
        print("Moving Base Left\Clockwise")
        
    def baseRight(self, event):
        self.cmd = [0,2,self.light]
        self.sendCmd(self.cmd)
        print("Moving Base Right\Anti-Clockwise")
        
    def shoulderUp(self, event):
        self.cmd = [64,0,self.light]
        self.sendCmd(self.cmd)
        print("Moving Shoulder Up")
        
    def shoulderDown(self, event):
        self.cmd = [128,0,self.light]
        self.sendCmd(self.cmd)
        print("Moving Shoulder Down")
        
    def elbowUp(self, event):
        self.cmd = [16,0,self.light]
        self.sendCmd(self.cmd)
        print("Moving Elbow Up")
        
    def elbowDown(self, event):
        self.cmd = [32,0,self.light]
        self.sendCmd(self.cmd)
        print("Moving Elbow Down")
        
    def wristUp(self, event):
        self.cmd = [4,0,self.light]
        self.sendCmd(self.cmd)
        print("Moving Wrist Up")
        
    def wristDown(self, event):
        self.cmd = [8,0,self.light]
        self.sendCmd(self.cmd)
        print("Moving Wrist Down")
        
    def handOpen(self, event):
        self.cmd = [2,0,self.light]
        self.sendCmd(self.cmd)
        print("Opening Gripper")
        
    def handClose(self, event):
        self.cmd = [1,0,self.light]
        self.sendCmd(self.cmd)
        print("Closing Gripper")
        
    def ledOnOFF(self, event):
        self.ticks = 0
        self.light = not self.light
        self.cmd = [0,0,self.light]
        self.sendCmd(self.cmd)
        print("LED", self.light)
    
    def ledOn(self):
        self.ticks = 0
        self.light = 1
        self.cmd = [0,0,1]
        self.stopArm()
        print("LED ON")
    
    def ledOff(self):
        self.ticks = 0
        self.light = 0
        self.cmd = [0,0,0]
        self.stopArm()
        print("LED OFF")
        
    def buttonRelease(self, event):
        self.stopArm()

    def stopArm(self):
        if self.rec:
            if self.ticks == 0:
                self.listbox.insert(END, str(0) + ":" + str(self.cmd))
            else:
                self.listbox.insert(END, str(round((time.time()- self.ticks),1)) + ":" + str(self.cmd))
        self.sendCmd([0,0,self.light])

    def askopenfilename(self):
        # get filename
        filename = tkFileDialog.askopenfilename(**self.file_opt)
        if filename:
            fo = open(filename, "r")
            tmpList = fo.read().split("\n")
            if len(tmpList) > 0:
                self.listbox.delete(0,END)
                for idx in range(0, len(tmpList)):
                    self.listbox.insert(END, tmpList[idx])                
            # Close opened file
            fo.close()
            
    def asksaveasfilename(self):
        if self.listbox.size() > 0:
            # get filename
            filename = tkFileDialog.asksaveasfilename(**self.file_opt)
            if filename:
                fo = open(filename, "w")
                for idx in range(0, self.listbox.size()):
                    fo.write(self.listbox.get(idx));
                    if idx < (self.listbox.size()-1):
                        fo.write("\n");
                # Close opened file
                fo.close()
        else:
            tkMessageBox.showerror ("An Error has occurred!", "Nothing has been record to be saved!")
            
    def about(self):
        tkMessageBox.showinfo("About USB Robotic Arm", """This is a python script that connect to the Maplin (A37JN) \ Velleman
KSR10 USB robotic arm and displays a simple GUI to control it.""")
        
    def record(self):
        self.rec = 1
        self.recButtonOn.config(state=DISABLED)
        self.recButtonOff.config(state=NORMAL)
        
    def pause(self):
        self.rec = 0
        self.recButtonOn.config(state=NORMAL)
        self.recButtonOff.config(state=DISABLED)
        
    def clear(self):
        self.listbox.delete(0,END)
        
    def play(self):
        self.recButtonOn.config(state=DISABLED)
        self.recButtonOff.config(state=DISABLED)
        self.recButtonClear.config(state=DISABLED)
        self.rec = 0
        self.ticks = 0
        for idx in range(0, self.listbox.size()):
            tmpList = self.listbox.get(idx).split(':')
            cmdlist = tmpList[1].strip("[]").split(',')
            tmp = [int(cmdlist[0]),int(cmdlist[1]),int(cmdlist[2])]
            self.sendCmd(tmp)
            duration = float(tmpList[0])
            if duration == 0:
                self.light = int(cmdlist[2])
            else:
                time.sleep(duration)
                self.stopArm()
        self.recButtonOn.config(state=NORMAL)
        self.recButtonOff.config(state=DISABLED)
        self.recButtonClear.config(state=NORMAL)
    
    def setStatus(self, value):
        self.status.itemconfig(self.g, fill="")
        self.status.itemconfig(self.y, fill="")
        self.status.itemconfig(self.o, fill="")
        self.status.itemconfig(self.r, fill="")
        if (value >= 4):
            self.status.itemconfig(self.g, fill="green")
        if (value >= 3):
            self.status.itemconfig(self.y, fill="yellow")
        if (value >= 2):
            self.status.itemconfig(self.o, fill="orange")
        if (value >= 1):
            self.status.itemconfig(self.r, fill="red")
        
def center(win):
    win.update_idletasks()
    w = win.winfo_screenwidth()
    h = win.winfo_screenheight()
    size = tuple(int(_) for _ in win.geometry().split('+')[0].split('x'))
    x = ((w/2) - (size[0]/2))
    y = ((h/2) - (size[1]/2))
    win.geometry("%dx%d+%d+%d" % (size + (x, y)))
    
def run(command):
    fin, fout =os.popen2(command)
    fin.close()
    output = fout.read()
    exitcode = fout.close()
    return output

root = Tk()
# On Windows you may need to specify a path to libusb dll
# If the lib usb dll is in the same place as this scipt the uncomment the line below 
#backend = usb.backend.libusb1.get_backend(find_library=lambda x: "libusb-1.0.dll")
# Else specify a path like below.  
#backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:\\PathToLib\\libusb-1.0.dll")

# Allocate the name 'RobotArm' to the USB device
RobotArm = usb.core.find(idVendor=0x1267, idProduct=0x000)
#RobotArm = usb.core.find(idVendor=0x1267, idProduct=0x001)

#Check if the arm is detected and warn if not
if RobotArm is None:
    raise ValueError("USB arm can not be found")
# Create Form Items
app = App(root)
# Center Main Window
center(root)
# Set Icon
if "nt" == os.name:
    root.iconbitmap(default="RoboticArm.ico")
else:
    root.wm_iconbitmap(bitmap = "@RoboticArm.xbm")
# turns auto repeat off if is set to on
if "posix" == os.name:
    repeat = run("xset q | grep 'repeat:' | awk '{ print $3; }'").strip()
    if repeat == "on":
        os.system("xset r off")
        print("turning off auto repeat")
# Show Form
root.mainloop()
# reset auto repeat
if repeat == "on":
    os.system("xset r on")
    print("turning on auto repeat")
