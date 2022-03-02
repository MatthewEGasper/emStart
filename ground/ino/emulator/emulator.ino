#include <Servo.h>

#define EARTH_AZ_SERVO  2
#define EARTH_EL_SERVO  3
#define GROUND_AZ_SERVO  4
#define GROUND_EL_SERVO  5

#define EARTH_AZ_OFFSET 0
#define EARTH_EL_OFFSET 0
#define GROUND_AZ_OFFSET 0
#define GROUND_EL_OFFSET 0

Servo earth_az_servo;
Servo earth_el_servo;
Servo ground_az_servo;
Servo ground_el_servo;

char earth_command_packet[13];
char ground_command_packet[13];
char earth_command_packet_old[13];
char ground_command_packet_old[13];

int earth_az = EARTH_AZ_OFFSET;
int earth_el = EARTH_EL_OFFSET;
int ground_az = GROUND_AZ_OFFSET;
int ground_el = GROUND_EL_OFFSET;

void setup() {
  Serial.begin(9600); //PC
  
  Serial1.begin(600); //Earth
  earth_az_servo.attach(EARTH_AZ_SERVO);
  earth_el_servo.attach(EARTH_EL_SERVO);

  Serial2.begin(600); //Ground
  ground_az_servo.attach(GROUND_AZ_SERVO);
  ground_el_servo.attach(GROUND_EL_SERVO);
}

void loop() {
  if(Serial1.available()) { 
    Serial1.readBytes(earth_command_packet,13);
    if(ground_command_packet[11] == 0x0F || ground_command_packet[11] == 0x1F){ //STOP or STATUS
      char response_packet[12];
      for(int i=0; i<11; i++){
        response_packet[i] = earth_command_packet_old[i];
      }
      response_packet[11] = 0x20;
      Serial1.write(response_packet);
      
    }else if(earth_command_packet[11] == 0x2F){  //SET
      char azimuth[4];
      char elevation[4];
      for(int i=0; i<4; i++){
        azimuth[i] = earth_command_packet[i+1];
        elevation[i] = earth_command_packet[i+6];
      }
      earth_az = atol(azimuth) + EARTH_AZ_SERVO;
      earth_el = atol(elevation) + EARTH_EL_SERVO;
    }
    for(int i=0; i<13; i++){
      earth_command_packet_old[i] = earth_command_packet[i];
    }
    //CODE FOR MOVING CONTROLLING EARTH SERVOS HERE
  }
  if(Serial2.available()) {
    Serial2.readBytes(ground_command_packet,13);
    if(ground_command_packet[11] == 0x0F || ground_command_packet[11] == 0x1F){ //STOP or STATUS
      char response_packet[12];
      for(int i=0; i<11; i++){
        response_packet[i] = ground_command_packet_old[i];
      }
      response_packet[11] = 0x20;
      Serial2.write(response_packet);
      
    }else if(ground_command_packet[11] == 0x2F){  //SET
      char azimuth[4];
      char elevation[4];
      for(int i=0; i<4; i++){
        azimuth[i] = earth_command_packet[i+1];
        elevation[i] = earth_command_packet[i+6];
      }
      ground_az = atol(azimuth) + GROUND_AZ_SERVO;
      ground_el = atol(elevation) + GROUND_EL_SERVO;
    }
    for(int i=0; i<13; i++){
      ground_command_packet_old[i] = ground_command_packet[i];
    }
    //CODE FOR MOVING CONTROLLING GROUND SERVOS HERE
  }
}

/*
void set_servo(int azimuth, int elevation){
  int azimuth_set = azimuth + AZIMUTH_OFFSET;
  int elevation_set = elevation + ELEVATION_OFFSET;
  if((azimuth_set >= 0)&&(azimuth_set <= 360)&&(elevation_set >= 0)&&(elevation_set <= 90)){
      azimuth_servo.write(azimuth_set);
      elevation_servo.write(elevation_set);
  }
}*/
