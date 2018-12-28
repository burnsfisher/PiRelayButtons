
# WB1FJ Antenna Control

This is a GUI to control relays that switch a software defined
radio connected to a telemetry computer and a TS-2000 among an
omni dual band satellite antenna, an LEO Pack 70cm and 2m beam, 
and a dual-band J-pole for local work

##Relays:

Preamp70:  Preamp on 70cm Beam
Preamp2m:  Preamp on 2m Beam
Beam70: Switch 70cm Beam to TS2K bus or SDR Bus
Beam2m: Switch  2m  Beam to TS2K bus or SDR Bus
TS2K: Switch TS-2000 to TS2K bus or dual band J-pole
SDR: Switch SDR to SDR Bus or Lindenblad (Omni)


V/u Satellite COM: 	Preamp70 on
			Preamp2m off
			Beam70: TS2K Bus
			Beam2m: TS2K Bus
			TS2K: TS2K
			SDR: Omni

U/v Satellite COM:  	TS2K70->Beam70
			TS2k2m->Beam2m
			Preamp70 off
			Preamp2m on
			Telem SDR->Lindy

Local Repeater		TS2K70->Mixer/Jpole (Initially Beam70)
			TS2K2m->Mixer/Jpole (Initially Beam2m)
			Preamp70 off
			Preamp2m off

V/u Satellite Telem	TS2K70 (open/dummy)
			TS2K2m->Beam2m
			Preamp70 on
			Preamp2m off
			Telem SDR->Beam70

U/v Satellite Telem	TS2K70->Beam70
			TS2K2m  (open/dummy)
			Preamp70 off
			Preamp2m on
			Telem SDR->Beam2m


Relays:

VHF beam -> TS2K or SDR
UHF beam -> TS2K or SDR

TS2K-VHF/UHF -> Diplexer J-pole or Relays above

SDR -> Omni or Relays above

