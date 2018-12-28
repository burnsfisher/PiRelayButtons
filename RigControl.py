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
#Local Repeater: 	  Preamp70 off
#		    Preamp2m off
#		    Beam70: TS2K Bus
#		    Beam2m: TS2K Bus
#		    TS2K: J-pole
#		    SDR: Omni
#
#UHF Beam Telem: 	  Preamp70: on
#		    Preamp2m: off
#		    Beam70: SDR Bus
#		    Beam2m: TS2K Bus
#		    TS2K: TS2K Bus
#		    SDR: SDR Bus
#
#VHF Beam Telem: 	  Preamp70 off
#		    Preamp2m on
#		    Beam70: TS2K Bus
#		    Beam2m: SDR Bus
#		    TS2K: TS2K
#		    SDR: SDR Bus



#import tkinter as tk
from tkinter import *
import RPi.GPIO as GPIO

class Relay:
    def set(self,state):
        self.state= state
        GPIO.output(self.gpioNum,self.state)
        
    def get(self):
        return self.state
        
    def __init__(self,gpioNum,initialState):
        self.gpioNum = gpioNum
        GPIO.setup(self.gpioNum,GPIO.OUT)
        self.set(initialState)
    

GPIO.setmode(GPIO.BOARD)

Off=True
On=False
TS2K=True
SDR=False
Beam=False
JPole=True
Omni=True
#Define the GPIOs for various relays
relayPreamp70 = Relay(23,Off)
relayPreamp2m = Relay(29,On)
relay2mBeamTS2KorSDR = Relay(31,TS2K)
relay70BeamTS2KorSDR = Relay(33,TS2K)
relayTS2KbeamOrJPole = Relay(35,Beam)
relaySDRbeamOrOmni = Relay(37,Omni)

relaySpare1 = Relay(21,On)
relaySpare2 = Relay(19,On)

RelayList = [relayPreamp70,relayPreamp2m,relay2mBeamTS2KorSDR,relay70BeamTS2KorSDR,relayTS2KbeamOrJPole,
             relaySDRbeamOrOmni]
NumberOfRelays = 6
#Button Values
UvButtonNum=0
VuButtonNum=1
RepeaterButtonNum=2
UHFTlmButtonNum=3
VHFTlmButtonNum=4

RelayActionsForButton = [
    #2mPre 70Pre 2mBeam 70Beam TS2KAnt SDRAnt
    [Off,  On,   TS2K,  TS2K,   Beam,  Omni], #UVButton
    [On,   Off,  TS2K,  TS2K,   Beam,  Omni], #VUButton
    [Off,  Off,  TS2K,  TS2K,   JPole, Omni], #Repeater
    [On,   Off,  TS2K,  SDR,    Beam,  Beam], #UTelemButton
    [Off,  On,   SDR,   TS2K,   Beam,  Beam], #VTelemButton
    ]


## GUI definitions

win = Tk()
CurrentButton=IntVar()
CurrentButton.set=UvButtonNum
win.title="BF"
#myFont = tk.font(family='Helvitica', size = 12, weight = "bold")
#Button Event functions

def Leave():
    GPIO.cleanup()
    exit(0)
    
def RelaySwitch():
    thisButtonIndex = CurrentButton.get()
    print("Button number ",thisButtonIndex)
    RelaySettings = RelayActionsForButton[thisButtonIndex]
    for i in range(NumberOfRelays):
        thisRelay = RelayList[i]
        thisRelay.set(RelaySettings[i])
        print("Relay #",i,"is set to ",RelaySettings[i])
    
##    thisButton = AllButtons[thisButtonIndex]
#### Widgets

SatComUvButton = Radiobutton(win,text = "U/v Satcom",command=RelaySwitch)
SatComUvButton.pack(anchor=W)
SatComUvButton.config(variable=CurrentButton,value=UvButtonNum,indicatoron=False)

SatComVuButton = Radiobutton(win,text = "V/u Satcom",command=RelaySwitch)
SatComVuButton.pack(anchor=W)
SatComVuButton.config(variable=CurrentButton,value=VuButtonNum,indicatoron=False)

RepeaterButton = Radiobutton(win,text = "Local Repeater",command=RelaySwitch)
RepeaterButton.pack(anchor=W)
RepeaterButton.config(variable=CurrentButton,value=RepeaterButtonNum,indicatoron=False)

SatTlmVButton = Radiobutton(win,text = "VHF Telemetry",command=RelaySwitch)
SatTlmVButton.pack(anchor=W)
SatTlmVButton.config(variable=CurrentButton,value=VHFTlmButtonNum,indicatoron=False)

SatTlmUButton = Radiobutton(win,text = "UHF Telemetry",command=RelaySwitch)
SatTlmUButton.pack(anchor=W)
SatTlmUButton.config(variable=CurrentButton,value=UHFTlmButtonNum,indicatoron=False)


ExitButton = Radiobutton(win,text = "Exit",command=Leave,variable=CurrentButton,value=99,indicatoron=False)
ExitButton.pack(anchor=W)

AllButtons=[SatComUvButton,SatComVuButton]
mainloop()
