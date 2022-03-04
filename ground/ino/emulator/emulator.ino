#include <Servo.h>

#define EARTH 0
#define GROUND 1

#define EARTH_AZ_SERVO  2
#define EARTH_EL_SERVO  3
#define GROUND_AZ_SERVO 4
#define GROUND_EL_SERVO 5

Servo az_servos[2];
Servo el_servos[2];

char command_packet[13];
char set_command_packet[13] = {0x57, 0x30, 0x39, 0x36, 0x37, 0x1, 0x30, 0x38, 0x37, 0x34, 0x1, 0x2F, 0x20};
char status_command_packet[13] = {0x57, 0x0, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1F, 0x20};
char ppd = 2;

float az[2] = {0, 0};
float el[2] = {0, 0};

float az_offsets[2] = {0, 0};
float el_offsets[2] = {0, 0};

void setup() {
  Serial.begin(9600); // computer
  
  Serial1.begin(600); // earth
  az_servos[EARTH].attach(EARTH_AZ_SERVO);
  el_servos[EARTH].attach(EARTH_EL_SERVO);

  Serial2.begin(600); // ground
  az_servos[GROUND].attach(GROUND_AZ_SERVO);
  el_servos[GROUND].attach(GROUND_EL_SERVO);
  
  // SIMULATION TESTS
  // process_command_packet(EARTH, set_command_packet);
  // process_command_packet(EARTH, status_command_packet);
}

void loop() {
  if(Serial1.available() >= 13) {
    Serial1.readBytes(command_packet, 13);
    process_command_packet(EARTH, command_packet);
  }
  
  if(Serial2.available() >= 13) {
    Serial2.readBytes(command_packet, 13);
    process_command_packet(GROUND, command_packet);
  }
}

void process_command_packet(int ID, char pkt[]) {
  if(ID == EARTH) {
    Serial.print("Earth command packet received: [");
  } else if(ID == GROUND) {
    Serial.print("Ground command packet received: [");
  }

  for(int i=0; i<13; i++) {
    if(i != 0) Serial.print(", ");
    Serial.print("0x");
    Serial.print(pkt[i], HEX);
  }
  Serial.println("]");
  
  if(pkt[11] == 0x0F || pkt[11] == 0x1F) {
    // STOP or STATUS command
    Serial.println("STOP / STATUS");
    generate_response_packet(ID);
  } else if(pkt[11] == 0x2F) {
    // SET command
    Serial.println("SET");
    
    char new_az[4], new_el[4];

    for(int i=0; i<4; i++){
      new_az[i] = pkt[i+1];
      new_el[i] = pkt[i+6];
    }
    
    az[ID] = (atol(new_az) / ppd) - 360;
    el[ID] = (atol(new_el) / ppd) - 360;

    Serial.print("Azimuth:   ");
    Serial.println(az[ID]);
    Serial.print("Elevation: ");
    Serial.println(el[ID]);

    set_servos(ID);
  }
}

void generate_response_packet(int ID) {
  char pkt[12] = {0x57, 0x0, 0x0, 0x0, 0x0, ppd, 0x0, 0x0, 0x0, 0x0, ppd, 0x20};
  String rsp_az, rsp_el;
  int az_c, el_c;
  
  // set the H values
  rsp_az = "00000" + String(az[ID] + 360, 10);
  az_c = rsp_az.indexOf('.');
  pkt[1] = rsp_az[az_c - 3] - '0';
  pkt[2] = rsp_az[az_c - 2] - '0';
  pkt[3] = rsp_az[az_c - 1] - '0';
  pkt[4] = rsp_az[az_c + 1] - '0';

  // set the V values
  rsp_el = "00000" + String(el[ID] + 360, 10);
  el_c = rsp_el.indexOf('.');
  pkt[6] = rsp_el[el_c - 3] - '0';
  pkt[7] = rsp_el[el_c - 2] - '0';
  pkt[8] = rsp_el[el_c - 1] - '0';
  pkt[9] = rsp_el[el_c + 1] - '0';

  if(ID == EARTH) {
    Serial1.write(pkt, 12);
    Serial.print("Earth response packet sent: [");
  } else if(ID == GROUND) {
    Serial2.write(pkt, 12);
    Serial.print("Ground response packet sent: [");
  }
  
  for(int i=0; i<12; i++) {
    if(i != 0) Serial.print(", ");
    Serial.print("0x");
    Serial.print(pkt[i], HEX);
  }
  Serial.println("]");
}

void set_servos(int ID){
  int set_az = az[ID] + az_offsets[ID];
  int set_el = el[ID] + el_offsets[ID];
  
  if((set_az >= 0) && (set_az <= 360) && (set_el >= 0) && (set_el <= 90)){
    az_servos[ID].write(set_az);
    el_servos[ID].write(set_el);
  } else {
    Serial.println("Tried to set servos to bad value!");
  }
}
