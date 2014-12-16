Snake-MSP430-Assembly
=====================

An implementation of the game 'snake'. Written for use on the msp430, developed using the IAR workbench. 
It's all in assembly, because yay course requirements.

I honestly didnt have a wiring diagram layed out when i was putting the project together, and i don't intend to createon now.
For future reference though, it might be best to at least give a slightly detailed description here.

Parts Used:
One MSP430 Launchpad with a MSP430-G2553 microprocessor powering the whole thing.
One 8x8 LED matrix
Two 3-8 decoders, model number M74HC238B1 specifically.
Two 7404 inverter ICs
One 7805 5V regulator
A battery pack that holds 4 AA batteries
4 push buttons
lotsa wires


Pins used on the Launchpad:
Most of everything should be written down as comments inside the program file, so you'll have to read really carefully if 
something i write here is incorrect.
Pins 1.0, 1.1, 1.2 are used for the decoder that will handle getting power to the LED matrix. They are tied into input A, B, C,
  on the decoder, respectively. 
Pins 2.0, 2.1, 2.2 are used for the decoder that will provide a ground for the matrix. they are tied to A, B, and C of the 
    second decoder.
Pins 1.4, 1.5, 1.6, 1.7 are used as inputs, and are connected to 4 push buttons that will be used as input.
Pin 2.4 is used to control the enable-High pin on the second decoder. (without this there is erratic display)


General Wiring Info That Seems Important to Mention:
  So the general idea is that the msp430 takes inputs from 4 push buttons, and outputs on 7 pins. 3 per decoder,
  and an extra one for the second decoder (the decoder that outputs to the inverters) to disable it temporarily. 
  
  The first inverter handles power to the matrix, the second decoder runs to inverters, which handles grounding the matrix.
  
  The battery pack runs to the regulator, which then is connected to the launchpad. All power requirements for other parts are 
  handled by going through the VCC and Ground pins on the launchpad.
  
  What else... the push buttons are meant to send a high signal when pressed, so they should be connected to VCC on one side.
  

I'm going to hope that's enough information to get the ball rolling if myself or anyone else has to recreate this.
