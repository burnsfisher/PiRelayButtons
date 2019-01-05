
# WB1FJ Antenna Control aka Relay Button Control

This is a GUI to control relays using a button box.  The names of the relays are all based on my particular use of this software.  I am using it to drive relays and preamps that set up my ham radio rig the way I want it.  You can use it for anything, of course.

From here on, we have the description of *MY* use.  My intent is to switch a software defined radio receiver (telemetry) and a Kenwood TS-2000 (TS2K) in various combinations with an omni dual band satellite antenna, an LEO Pack 70cm and 2m beam,  and a dual-band J-pole for local work.

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

In addition there are some checkboxes for the preamps which are updated to
match the preamp state when you click on a configuration.  However they can
also be checked or unchecked to override the default for the preamps.

Schematic of the coax relays as a [PNG File](AntennaSwitcher.png) or a [PDF File](AntennaSwitcher.pdf).  Note that the 
schematics do not show that each relay has a flyback diode across it.

