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

  //Serial setup:
  Serial.begin(9600);
  while (!Serial) {
    delay(1);
  }

  //software serial setup:
  mySerial.begin(9600);

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
 // delay(5);
  //Serial.println(mySerial.available());
  char receivedString[10];
  int packetIndex=0;
  if (mySerial.available()) {
    char c = mySerial.read();
    //Serial.print(c);
    if (c == 'U') {
      delay(5);  //allow time for remainder of message to arrive
      bool isValid=true;
      while(c=='U'){
        c=mySerial.read();// filter out following 2 sychronization 'U's
      }
      char radioPacket[8];
      for(int i=0; i<4; i++){
        if(c < '0'|| c > '9'){
          isValid=false;
          Serial.print("warning, invalid number recieved, "+String(c));
          break;
        }
        Serial.print("got "+String(c));
        radioPacket[i]=c;
        c=mySerial.read();
      }
      if (c!=';'){
        isValid=false;
        Serial.print("warning expected ';' recieved "+String(c));
      }
      if (isValid){
        radioPacket[4]=0;
        Serial.println("transmitting: " + String(radioPacket));
        rf95.send((uint8_t *)radioPacket, 5);
        rf95.waitPacketSent();
      }
    }
  }
}

