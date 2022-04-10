//Radio Libraries:
#include <SPI.h>
#include <RH_RF95.h>
//#include <Wire.h>

#include <SoftwareSerial.h>


//Radio setup:
#if defined (__AVR_ATmega328P__)  // UNO or Feather 328P w/wing
#define RFM95_INT     3  // 
#define RFM95_CS      4  //
#define RFM95_RST     2  // "A"
#define LED           13
#endif


// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 915.0


SoftwareSerial mySerial(6, 5); // RX, TX

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

//integer to store the angle of the servo recieved from MKR ZERO
int pos = 0;

void setup()
{

  //Radio setup:
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  

  Serial.begin(9600);
  while (!Serial) {
    delay(1);
  }


  mySerial.begin(9600);

  delay(100);

  //Serial.println("Feather LoRa TX Test!");

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    //Serial.println("Uncomment '#define SERIAL_DEBUG' in RH_RF95.cpp for detailed debug info");
    while (1);
  }
  Serial.println("LoRa radio init OK!");

  //i2c setup:
//  Wire.begin(4);                // join i2c bus with address #4
//  Wire.onReceive(receiveEvent); // register event

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    //Serial.println("setFrequency failed");
    while (1);
  }
  //Serial.print("Set Freq to: "); //Serial.println(RF95_FREQ);

  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);
}

void loop() {

  //add delay for loop stability:
  delay(50);
  
  if(mySerial.available()){
    receiveEvent(mySerial.available());
  }
  

}

void receiveEvent(int howMany) {
  Serial.println("got "+String(mySerial.available())+"bytes");
  while (1 < mySerial.available()) { // loop through all but the last
    char c = mySerial.read(); // receive byte as a character
    if(c=='U'){
      char radioPacket[8];
      int packetIndex=0;
      while(c!=';'){
        
        c = mySerial.read(); // receive byte as a character
        if(c!="U"){
          radioPacket[packetIndex]=c;
          packetIndex++;
        }
      }
      radioPacket[packetIndex-1]=0;
      Serial.println("transmitting: "+String(radioPacket));
      rf95.send((uint8_t *)radioPacket, packetIndex+1);
      rf95.waitPacketSent();

    }
   // Serial.print(c);         // print the character
  }
  //int pos = mySerial.read();    // receive byte as an integer
  //Serial.println(pos);         // print the integer
  /*String posString = String(sprintf("%c%c%c%c",mySerial.read(),mySerial.read(),mySerial.read(),mySerial.read()));
  
  Serial.println("Position: " + posString);
  
  //create radio packet with 3 numbers, will eventually be 0 to 360 degrees
  char radiopacket[4] = {posString[0], posString[1], posString[2], 0};

  radiopacket[3] = 0;
  //delay(5);
  //send the packet:*/
  //rf95.send((uint8_t *)radiopacket, 4);
  //delay(5);
  //wait while the packet is sending:
 // rf95.waitPacketSent();
}
/*
void receiveEvent(int howMany)
{
  //Serial.println("1234567890");
  while (1 < Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    Serial.print(c);         // print the character
  }
  int pos = 765;//Wire.read();    // receive byte as an integer
  Serial.println(pos);         // print the integer
  String posString = String(pos);
  if (pos <= 9)
  {
    posString = "00" + posString;
  }
  if (pos > 9 && pos <= 99)
  {
    posString = "0" + posString;
  }
  //Serial.println("Position: " + posString);

  //create radio packet with 3 numbers, will eventually be 0 to 360 degrees
  char radiopacket[4] = {posString[0], posString[1], posString[2], '0'};
  //Serial.print("Sending "); //Serial.println(radiopacket);
  //set the last char to 0 for some reason:
  radiopacket[3] = 0;
  //send the packet:
  rf95.send((uint8_t *)radiopacket, 4);
  //wait while the packet is sending:
  rf95.waitPacketSent();
}
*/
