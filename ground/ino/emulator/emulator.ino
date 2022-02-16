#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial portOne(0, 1);
//SoftwareSerial portTwo(8, 9);
char message[13];

void setup() {
   Serial.begin(9600);
   while (!Serial) {}
   Serial.println("I think I am working!");
   portOne.begin(9600);
   //portTwo.begin(9600);
}

void loop() {
   while (Serial.available() > 0) {
    int red = Serial.readBytes(message, 13);
    
    //**Verification of Received Data Over Serial**
    Serial.print("Message is: ");
    for(int i=0; i<13; i++){
      Serial.print(message[i, HEX]);
    }
    Serial.println();
    
    //STOP--Packet 0 (0x57) and 11(0x0F) end byte (0x20)
    if(message[11] == 0x0F){
      Serial.println("STOP");
    //STATUS--Packet 0 (0x57) and 11(0x1F) end byte (0x20)
    }else if(message[11] == 0x1F){
      Serial.println("STATUS");
    //SET--Packet 0 (0x57) <1-4>H <6-9>V and 11(0x2F) end byte (0x20)
    }else if(message[11] == 0x2F){
      char height[4];
      char vertical[4];
      
      for(int i=; i<4; i++){
        height[i] = message[1+i];
        vertical[i] = message[6+i];
      }
      
      Serial.println("SET:");
      
      Serial.print("Height = ");
      for(int i=0; i<4; i++){
        Serial.print(height[i], HEX);
      }
      Serial.println();
      Serial.print("Vertical = ");
      for(int i=0; i<4; i++){
        Serial.print(veritcal[i], HEX);
      }
      Serial.println();
    }
    
  }
}
