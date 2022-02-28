#include <Servo.h>
#include <SoftwareSerial.h>

//setup parameters for azimuth and elevation servos
#define AZIMUTH_SERVO_PIN 6
#define ELEVATION_SERVO_PIN 5

#define AZIMUTH_OFFSET 0
#define ELEVATION_OFFSET 0

Servo azimuth_servo;
Servo elevation_servo;

int azimuth_set = 0;
int elevation_set = 0;

SoftwareSerial portOne(0, 1);
//SoftwareSerial portTwo(8, 9);
char message[13];

void setup() {
   Serial.begin(9600);
   while (!Serial) {}
   Serial.println("I think I am working!");
   portOne.begin(9600);
   //portTwo.begin(9600);

  //servo setup
   azimuth_servo.attach(AZIMUTH_SERVO_PIN);
   elevation_servo.attach(ELEVATION_SERVO_PIN);
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
      portOne.println("STOP");
      portOne.print("stop");
    //STATUS--Packet 0 (0x57) and 11(0x1F) end byte (0x20)
    }else if(message[11] == 0x1F){
      portOne.println("STATUS");
      portOne.print("status");
    //SET--Packet 0 (0x57) <1-4>H <6-9>V and 11(0x2F) end byte (0x20)
    }else if(message[11] == 0x2F){
      char height[4];
      char vertical[4];
      
      for(int i=0; i<4; i++){
        height[i] = message[1+i];
        vertical[i] = message[6+i];

      }

      //This is where the servo's position will be set
      //set_servo();
      
      Serial.println("SET:");
      
      Serial.print("Height = ");
      for(int i=0; i<4; i++){
        Serial.print(height[i], HEX);
      }
      Serial.println();
      Serial.print("Vertical = ");
      for(int i=0; i<4; i++){
        Serial.print(vertical[i], HEX);
      }
      Serial.println();
    }
    
  }
}
void set_servo(int azimuth, int elevation)
{
  int azimuth_set = azimuth + AZIMUTH_OFFSET;
  int elevation_set = elevation + ELEVATION_OFFSET;
  if((azimuth_set >= 0)&&(azimuth_set <= 360)&&(elevation_set >= 0)&&(elevation_set <= 90))
  {
      azimuth_servo.write(azimuth_set);
      elevation_servo.write(elevation_set);
  }
}
