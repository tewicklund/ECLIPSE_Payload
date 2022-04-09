//This Code will be put on the MKR_ZERO and will be responsible for driving the servo
//tutorial for i2c data transfer: https://www.arduino.cc/en/Tutorial/LibraryExamples/MasterWriter

#include <Servo.h>
#include <Wire.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Wire.begin(); // join i2c bus (address optional for master)
  
}

int pos = 0;    // variable to store the servo position

void loop() {
  for (pos = 0; pos <= 360; pos += 1) { // goes from 0 degrees to 360 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    
    //put code here to send the pos over i2c
    Wire.beginTransmission(4); // transmit to device #4
    Wire.write(pos);           //send int pos
    Wire.endTransmission();    // stop transmitting
    
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
  for (pos = 360; pos >= 0; pos -= 1) { // goes from 360 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    
    //put code here to send the pos over i2c
    Wire.beginTransmission(4); // transmit to device #4
    Wire.write(pos);           //send int pos
    Wire.endTransmission();    // stop transmitting
    
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
}
