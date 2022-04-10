//This Code will be put on the MKR_ZERO and will be responsible for driving the servo
//tutorial for i2c data transfer: https://www.arduino.cc/en/Tutorial/LibraryExamples/MasterWriter

#include <Servo.h>
#include <Wire.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards


void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Wire.begin(); // join i2c bus (address optional for master)
  Serial1.begin(9600);
  
}

int pos = 0;    // variable to store the servo position

void loop() {
  for (pos = 600; pos <=2400 ; pos += 1) { // goes from 0 degrees to 360 degrees
    // in steps of 1 degree
    myservo.writeMicroseconds(pos);              // tell servo to go to position in variable 'pos'
    Serial1.println("U"+String(pos)+";");
    
    //put code here to send the pos over i2c
    Wire.beginTransmission(4); // transmit to device #4
    Wire.write(pos);           //send int pos
    Wire.endTransmission();    // stop transmitting
    
    delay(30);                       // waits 15 ms for the servo to reach the position
  }
  for (pos = 2400; pos >= 600; pos -= 1) { // goes from 360 degrees to 0 degrees
    myservo.writeMicroseconds(pos);              // tell servo to go to position in variable 'pos'
    Serial1.println("UUU"+String(pos)+";;;");
    
    //put code here to send the pos over i2c
    Wire.beginTransmission(4); // transmit to device #4
    Wire.write(pos);           //send int pos
    Wire.endTransmission();    // stop transmitting
    
    delay(30);                       // waits 15 ms for the servo to reach the position
  }
}
