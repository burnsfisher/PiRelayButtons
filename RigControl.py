#
# WB1FJ Antenna Control
#
# This is a GUI to control relays that switch a software defined
# radio connected to a telemetry computer and a TS-2000 among an
# omni dual band satellite antenna, an LEO Pack 70cm and 2m beam, 
# and a dual-band J-pole for local work
#
#Relays:
#
#Preamp70:  Preamp on 70cm Beam
#Preamp2m:  Preamp on 2m Beam
#Beam70: Switch 70cm Beam to TS2K bus or SDR Bus
#Beam2m: Switch  2m  Beam to TS2K bus or SDR Bus
#TS2K: Switch TS-2000 to TS2K bus or dual band J-pole
#SDR: Switch SDR to SDR Bus or Lindenblad (Omni)
#
#   Button               Relay States
#
#U/v Satellite COM: Preamp70: off
#	            Preamp2m: on
#                   Beam70: TS2K Bus
#	            Beam2m: TS2K Bus
#		    TS2K: TS2K
#		    SDR: Omni
#
#V/u Satellite COM: Preamp70 on
#		    Preamp2m off
#		    Beam70: TS2K Bus
#		    Beam2m: TS2K Bus
#		    TS2K: TS2K
#		    SDR: Omni
#
#Local Repeater:    Preamp70 off
#		    Preamp2m off
#		    Beam70: TS2K Bus
#		    Beam2m: TS2K Bus
#		    TS2K: J-pole
#		    SDR: Omni
#
#UHF Beam Telem:    Preamp70: on
#		    Preamp2m: off
#		    Beam70: SDR Bus
#		    Beam2m: TS2K Bus
#		    TS2K: TS2K Bus
#		    SDR: SDR Bus
#
#VHF Beam Telem:   Preamp70 off
#		    Preamp2m on
#		    Beam70: TS2K Bus
#		    Beam2m: SDR Bus
#		    TS2K: TS2K
#		    SDR: SDR Bus


UDP_IP = "10.0.1.255"
UDP_PORT = 9932

#import tkinter as tk

import tkinter as tk
import RPi.GPIO as GPIO
import time
import sys
import socket

DebugRelaySet = False #Set true to get some printouts

class Relay: #This is for the Sunfounder/Huayao relay board where a high GPIO turns the relay coil off.
    
    # If you create a Relay instance with a checkbutton, that checkbutton is activated or deactivated
    # when the relay is turned on or off
    
    def __init__(self,gpioNum1,initialState,checkbutton=None):
        self.gpioNum = gpioNum1
        GPIO.setup(self.gpioNum,GPIO.OUT)
        self.fixButton=checkbutton
        self.set(initialState)
    def setAssociatedButton(self,button):
        #Associated Button's select or deselect method is called to match this
        #relay's state.  It also let's the button turn the relay on and off
        #rather than doing it here.
        self.fixButton=button

    def setOnly(self,state):
        #Set the relay without calling the button method.  Used by the button method itself
        self.state= state
        GPIO.output(self.gpioNum,not self.state) #High for off, low for on
        
    def set(self,state):
        self.setOnly(state)
        if self.fixButton is not None:
            if state:
                self.fixButton.select()
            else:
                self.fixButton.deselect()
        
    def get(self):
        return self.state
        

#Define values for the relays that name the purpose for the relay in that position

On=True #For Preamps (Default)
Off=False
TS2K=False #For Beam Bus TS2K End (Default)
SDR=True
Beam=True #For TS2k and SDR
JPole=False #For TS2K
Omni=False #For SDR


## GUI definitions

#Button Values
UvButtonNum=0
VuButtonNum=1
RepeaterButtonNum=2
UHFTlmButtonNum=3
VHFTlmButtonNum=4
VUTlmButtonNum=5
#Callback routines for checkbuttons.  They set the relay to the value of the checkbox

def Switch2mPreamp():
    RelayList[relayPreamp2m].setOnly(P2mValue.get()==1)
def Switch70Preamp():
    RelayList[relayPreamp70].setOnly(P70Value.get()==1)

#Define the relay index numbers for various relays
relayPreamp70 = 0
relayPreamp2m = 1 #ok
relay2mBeamTS2KorSDR = 2 #Ok
relay70BeamTS2KorSDR = 3 #ok
relayTS2KbeamOrJPole = 4 #ok
relaySDRbeamOrOmni = 5 #ok

GPIO.setmode(GPIO.BOARD) #Define GPIOs by board pin number
#Now define the pin numbers for each relay index
#relayPinNumbers=[5,7,11,13,15,8]
relayPinNumbers=[37,40,29,31,33,35] #These are for PiZero with SPI Screen

#Now create the relay objects for each relay
RelayList = []
for i in range (0,len(relayPinNumbers)):
    RelayList.append(Relay(relayPinNumbers[i],False))
            
#The following table tells what values to set each relay (columns) to for each configuration(row)
#Row numbers have to match the value passed to the variable in the radio buttons; column number
#must match the order of the relays in RelayList

RelayActionsForButton = [
    #70Pre 2mPre 2mBeam 70Beam TS2KAnt SDRAnt Spares <-Relays
    [Off,  On,   TS2K,  TS2K,   Beam,  Omni, Off, Off], #UVButton
    [On,   Off,  TS2K,  TS2K,   Beam,  Omni, Off, Off], #VUButton
    [Off,  Off,  TS2K,  TS2K,   JPole, Omni, Off, Off], #Repeater
    [On,   Off,  TS2K,  SDR,    Beam,  Beam, Off, Off], #UTelemButton
    [Off,  On,   SDR,   TS2K,   Beam,  Beam, Off, Off], #VTelemButton
    [On,   On,   SDR,   SDR,   JPole, JPole, Off, Off]  #VUTelemButton
    ]


#Here are callback routines for all the buttons and checkboxes
def Leave(): #This one is for the exit radio button
    GPIO.cleanup()
    sys.exit(1)

def RelayGroupSwitch(): #This is for all other radio buttons
    thisButtonIndex = CurrentButton.get()
    if(DebugRelaySet):
        print("Button number ",thisButtonIndex)
    RelaySettings = RelayActionsForButton[thisButtonIndex]
    for i in range(len(RelayList)):
        thisRelay = RelayList[i]
        thisRelay.set(RelaySettings[i])
        if(DebugRelaySet):
            print("Setting relay",i, "to", RelaySettings[i])



#Here is where we set up the layout for the screen

win = tk.Tk()
#win.geometry("200x200")
win.title("WB1FJ Antenna Switcher")
CurrentButton=tk.IntVar()
tk.Label(win,text="Configuration:").grid(row=0,columnspan=2,sticky=tk.W)

#Here are 2 checkboxes for preamps that are overrides of the standard values for a confiruration.
#For example, you can turn on the preamp while in the local repeater configuration.

tk.Label(win,text="Preamp Override:").grid(row=8,column=0,sticky=tk.E)
tk.Label(win,text="________________________________________________________________________________").grid(row=7,column=0,columnspan=2)

P70Value = tk.IntVar()
Preamp70Button = tk.Checkbutton(win,text="70Cm",variable=P70Value,command=Switch70Preamp)
Preamp70Button.grid(column=1,row=8)

P2mValue=tk.IntVar()
Preamp2mButton = tk.Checkbutton(win,text="2M",variable=P2mValue,command=Switch2mPreamp)
Preamp2mButton.grid(column=1,row=8,sticky=tk.W)

RelayList[relayPreamp70].setAssociatedButton(Preamp70Button) #Make sure when a configuration sets one of these relays,---
RelayList[relayPreamp2m].setAssociatedButton(Preamp2mButton) #...the checkbox matches


# Here are the radio buttons that let you choose the configuration--only one is active at a time.

SatComUvButton = tk.Radiobutton(win,text = "U/v Satcom",command=RelayGroupSwitch,selectcolor="Red")
SatComUvButton.config(variable=CurrentButton,value=UvButtonNum,indicatoron=False,width=30,pady=20)
SatComUvButton.grid(row=4,column=0)

SatComVuButton = tk.Radiobutton(win,text = "V/u Satcom",command=RelayGroupSwitch,selectcolor="Red")
SatComVuButton.grid(row=4,column=1,columnspan=1)
SatComVuButton.config(variable=CurrentButton,value=VuButtonNum,indicatoron=False,width=30,pady=20)


RepeaterButton = tk.Radiobutton(win,text = "Local Repeater",command=RelayGroupSwitch,selectcolor="Red")
RepeaterButton.grid(row=6,column=0,columnspan=1)
RepeaterButton.config(variable=CurrentButton,value=RepeaterButtonNum,indicatoron=False,width=30,pady=20)


SatTlmVButton = tk.Radiobutton(win,text = "VHF Telemetry",command=RelayGroupSwitch,selectcolor="Red")
SatTlmVButton.grid(row=5,column=0,columnspan=1)
SatTlmVButton.config(variable=CurrentButton,value=VHFTlmButtonNum,indicatoron=False,width=30,pady=20)

SatTlmUButton = tk.Radiobutton(win,text = "UHF Telemetry",command=RelayGroupSwitch,selectcolor="Red")
SatTlmUButton.grid(row=5,column=1,columnspan=1)
SatTlmUButton.config(variable=CurrentButton,value=UHFTlmButtonNum,indicatoron=False,width=30,pady=20)

SatTlmVUButton = tk.Radiobutton(win,text = "VU Telemetry",command=RelayGroupSwitch,selectcolor="Red")
SatTlmVUButton.grid(row=6,column=1,columnspan=1)
SatTlmVUButton.config(variable=CurrentButton,value=VUTlmButtonNum,indicatoron=False,width=30,pady=20)


ExitButton = tk.Radiobutton(win,text = "Exit",command=Leave,variable=CurrentButton,value=99,indicatoron=False)
ExitButton.grid(row=8,column=0,sticky=tk.W)

#Set the default button
CurrentButton.set(RepeaterButtonNum)
RelayGroupSwitch() #Set up everything for the above default button

DebugRelayID = False

#This is to make sure we know which relay is which
if DebugRelayID:
    for i in range(len(RelayList)):
        thisRelay = RelayList[i]
        thisRelay.set(True)
        print("Setting relay",i, "to True")
        time.sleep(1)

    for i in range(len(RelayList)):
        thisRelay = RelayList[i]
        thisRelay.set(False)
        print("Setting relay",i, "to False")
        time.sleep(1)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(.1)

while 1:
    win.update() # This allows me to do something else besides Tk.   Equiv to mainloop, but it returns
    try:
        databytes, addr = sock.recvfrom(128) # buffer size is 128 bytes
        datastr = (databytes.decode('UTF-8'))
        strList=datastr.split(',')
        downlink = int(float(strList[1]))
        print("AOS: downlink is ",strList[1])
        curBut = CurrentButton.get()
        if (downlink < 400):
            if(curBut == VuButtonNum):
                CurrentButton.set(UvButtonNum)
            if(curBut == UHFTlmButtonNum):
                CurrentButton.set(VHFTlmButtonNum)
        if (downlink >= 400):
            if(curBut == UvButtonNum):
                CurrentButton.set(VuButtonNum)
            if(curBut == VHFTlmButtonNum):
                CurrentButton.set(UHFTlmButtonNum)
        RelayGroupSwitch();
    except:
        pass

#win.mainloop()

UvButtonNum=0
VuButtonNum=1
RepeaterButtonNum=2
UHFTlmButtonNum=3
VHFTlmButtonNum=4
VUTlmButtonNum=5

