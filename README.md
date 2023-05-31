
# WB1FJ Antenna Control aka Relay Button Control

This is a GUI to control relays using a button box.  The names of the relays are all based on my particular use of this software.  I am using it to drive relays and preamps that set up my ham radio rig the way I want it.  You can use it for anything, of course.

From here on, we have the description of *MY* use.  My intent is to switch a software defined radio receiver (telemetry) and a Kenwood TS-2000 (TS2K) in various combinations with an omni dual band satellite antenna, an LEO Pack 70cm and 2m beam,  and a dual-band J-pole for local work.

Note that the latest version also listens for a UDP message specifying the uplink and downlink frequency of a satellite.  It looks at the downlink frequency and based on the band, changes the switches.  The message is one that could be sent via MacDoppler's scripting facility as of V2.39b1 when Don added the capability I needed.  Thanks Don!  It also can read the UDP message sent by the CSN Technologies S.A.T. satellite radio/rotator controller.

## Relays:
Name | Description
--------|----------
Preamp70|Preamp on 70cm Beam
Preamp2m|Preamp on 2m Beam
Beam70| Switch 70cm Beam to TS2K bus or SDR Bus
Beam2m| Switch  2m  Beam to TS2K bus or SDR Bus
TS2K| Switch TS-2000 to TS2K bus or dual band J-pole
SDR| Switch SDR to SDR Bus or Lindenblad (Omni)

## Button/relay combinations
Button                | Relay    |State
-----------|----------|----------
V/u Satellite COM |Preamp70|On
"                 |Preamp2m|Off
"			            |Beam70| TS2K Bus
"			            |Beam2m| TS2K Bus
"			            |TS2K| TS2K Bus
"			            |SDR| Omni
U/v Satellite COM |Preamp70|Off
"                 |Preamp2m|On
"			            |Beam70| TS2K Bus
"			            |Beam2m| TS2K Bus
"			            |TS2K| TS2K Bus
"			            |SDR| Omni
Local Repeater		|Preamp70|Off
"                 |Preamp2m|off
"			            |Beam70| TS2K Bus
"			            |Beam2m| TS2K Bus
"			            |TS2K| J-Pole
"			            |SDR| Omni
VHF Telemetry	Beam|Preamp70|Off
"                 |Preamp2m|On
"			            |Beam70| TS2K Bus
"			            |Beam2m| SDR Bus
"			            |TS2K| TS2K Bus
"			            |SDR| SDR Bus
UHF Telemetry	Beam|Preamp70|On
"                 |Preamp2m|Off
"			            |Beam70| SDR Bus
"			            |Beam2m| TS2K Bus
"			            |TS2K| TS2K Bus
"			            |SDR| SDR Bus
UV Telemetry    Beam|Preamp70|On
"                 |Preamp2m|On
"                                   |Beam70| SDR Bus
"                                   |Beam2m| SDR Bus
"                                   |TS2K| JPole
"                                   |SDR| SDR Bus

In addition there are some checkboxes for the preamps which are updated to
match the preamp state when you click on a configuration.  However they can
also be checked or unchecked to override the default for the preamps.

Schematic of the coax relays as a [PNG File](AntennaSwitcher.png) or a [PDF File](AntennaSwitcher.pdf).  Note that the 
schematics do not show that each relay has a flyback diode across it.

Not shown anywhere but necessary are another set of relays triggered by the 3V Raspberry Pi GPIO outputs which switch the 12V coils of the coax relays as well as switching 12V power to the preamps.  Here is an Amazon link to what I used:  https://www.amazon.com/gp/product/B07DNB2NGD.  However, this link appears broken, so try this (which appears similar):  https://www.amazon.com/Yizhet-Channel-Optocoupler-Raspberry-Channels/dp/B08Q3QKF3D

