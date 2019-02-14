#include <TinyWireS.h>
#include "avr/interrupt.h"

const byte SLAVE_ADDR = 0x40;
const byte NUM_BYTES = 4;
const uint8_t encoder_A = 3;
const uint8_t encoder_B = 4;
volatile long value = 0;
volatile uint8_t oldState = 0;
volatile uint8_t convert = 1;
volatile uint8_t state_B = 0;
volatile uint8_t state_A = 0;

volatile unsigned char data[NUM_BYTES] = {0,0,0,0};
volatile unsigned char dat[NUM_BYTES] = {3,8,9,2};
volatile uint8_t currentByte = 0;
void setup() {
    TinyWireS.begin(SLAVE_ADDR);
    TinyWireS.onRequest(requestISR);
    // initialize the digital pin as an output.
    pinMode(encoder_A, INPUT);       // PB3 is on A-line of Encoder
    pinMode(encoder_B, INPUT);       // PB4 is on B-line of Encoder       
    GIMSK = 0b00100000;       // turns on pin change interrupts
    PCMSK = 0b00001000;       // turn on interrupts on pins PB3
    sei();                    // enables interrupts
}

void loop() {
   // TinyWireS_stop_check();
 }


ISR(PCINT0_vect)
{
  state_B = digitalRead(encoder_B);
  state_A = digitalRead(encoder_A);
  if(state_A){
    if(state_B){
        value += 1; 
    }
    else{
        value -=1;
    }
  }
  else{
    if(state_B){
      value -=1;
    }
    else{
      value +=1;
    }
  }
}

void requestISR() {
        if(currentByte == 0){
            data[0] = (char)((abs(value) >> 24) & 0x7F) ;
            data[1] = (char)((abs(value) >> 16) & 0xFF) ;
            data[2] = (char)((abs(value) >> 8) & 0XFF);
            data[3] = (char)((abs(value) & 0XFF));
            if(value < 0){
              data[0] += 128;
            }  
          
        }
        TinyWireS.write(data[currentByte]);
        currentByte++;
        if(currentByte == 4){
          currentByte = 0; 
        }
}
