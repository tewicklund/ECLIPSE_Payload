//This Code will be put on the MKR_ZERO and will be responsible for driving the servo
//tutorial for i2c data transfer: https://www.arduino.cc/en/Tutorial/LibraryExamples/MasterWriter

#include <Servo.h>


Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards


void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial1.begin(9600);
  Serial.begin(9600);
}

int pos = 0;    // variable to store the servo position

void loop() {
  for (pos = 620; pos <=2400 ; pos += 10) { 
    // in steps of 1 degree
    myservo.writeMicroseconds(pos);              // tell servo to go to position in variable 'pos'
    
    //write a string formatted as "UUU####;;;" where the # are chars of numbers, example "UUU2038;;;"
    if (pos<999)
    {
      Serial1.println("UUU0"+String(pos)+";;;");
      Serial.println("UUU0"+String(pos)+";;;");
    }
    else
    {
      Serial1.println("UUU"+String(pos)+";;;");
      Serial.println("UUU"+String(pos)+";;;");
    }
    
    delay(300);                       // waits 15 ms for the servo to reach the position
  }
  for (pos = 2400; pos >= 620; pos -= 10) { 
    myservo.writeMicroseconds(pos);              // tell servo to go to position in variable 'pos'
    
    //write a string formatted as "UUU####;;;" where the # are chars of numbers, example "UUU2038;;;"
    if (pos<999)
    {
      Serial1.println("UUU0"+String(pos)+";;;");
      Serial.println("UUU0"+String(pos)+";;;");
    }
    else
    {
      Serial1.println("UUU"+String(pos)+";;;");
      Serial.println("UUU"+String(pos)+";;;");
    }
    delay(300);                       // waits 30 ms for the servo to reach the position
  }
}
