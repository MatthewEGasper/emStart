#include <Servo.h>

#define EARTH 0
#define GROUND 1

#define EARTH_AZ_SERVO  50
#define EARTH_EL_SERVO  51
#define GROUND_AZ_SERVO 52
#define GROUND_EL_SERVO 53

Servo az_servos[2];
Servo el_servos[2];

//                   {earth, ground}
float min_az_ms[2] = {500, 500};
float max_az_ms[2] = {2350, 2350};
float min_el_ms[2] = {900, 900};
float max_el_ms[2] = {1850, 1800};

char command_packet[13];
char ppd = 1;

float az[2] = {0, 0};
float el[2] = {90, 90};

void setup() {
  // host
  Serial.begin(9600);

  // earth
  Serial1.begin(600);
  az_servos[EARTH].attach(EARTH_AZ_SERVO);
  el_servos[EARTH].attach(EARTH_EL_SERVO);
  set_servos(EARTH);
  
  // ground
  Serial2.begin(600);
  az_servos[GROUND].attach(GROUND_AZ_SERVO);
  el_servos[GROUND].attach(GROUND_EL_SERVO);
  set_servos(GROUND);
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

//Function for Attenuator Control
void attenuatorControl(){
  //Calculate degrees accuracy of Ground station to Body in Space
  
  //if receiving antenna aim is aimed < ~5 degrees accuratly
  if(){
    //set power of attenuator High
  //else if receiving antenna aim is aimed < ~15 degrees accuratly
  }else if(){
    //set power of attenuator Medium
  //else if receiving antenna aim is aimed < ~30 degrees accuratly
  }else if(){
    //set power of attenuator Low
  }else(){
    //set power of attenuator Min
  }
}

void process_command_packet(int ID, char pkt[]) {
  if(ID == EARTH) {
    Serial.print("# Earth Command: ");
  } else if(ID == GROUND) {
    Serial.print("# Ground Command: ");
  }
  
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
  
  if(pkt[11] == 0x0F) {
    Serial.println("STOP");
    generate_response_packet(ID);
  } else if(pkt[11] == 0x1F) {
    Serial.println("STATUS");
    generate_response_packet(ID);
  } else if(pkt[11] == 0x2F) {
    Serial.println("SET");
    
    char new_az[4], new_el[4];

    for(int i=0; i<4; i++){
      new_az[i] = pkt[i+1] - '0';
      new_el[i] = pkt[i+6] - '0';
    }
    
    az[ID] = (new_az[0]*1000 + new_az[1]*100 + new_az[2]*10 + new_az[3] / ppd) - 360;
    el[ID] = (new_el[0]*1000 + new_el[1]*100 + new_el[2]*10 + new_el[3] / ppd) - 360;

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

void set_servos(int ID) {
  int set_az = az[ID];
  int set_el = el[ID];

  // translate azimuth angle to servo angle
  while(set_az >= 360) {
    set_az -= 360;
  }
  while(set_az < 0) {
    set_az += 360;
  }
  set_az *= -1;
  set_az += 360;

  // translate elevation angle to servo angle
  set_el *= -1;
  set_el += 90;

  // translate servo angles to ms
  set_az = set_az * ((max_az_ms[ID] - min_az_ms[ID]) / 360) + min_az_ms[ID];
  if(set_az > max_az_ms[ID]) {
    set_az = max_az_ms[ID];
  }
  if(set_az < min_az_ms[ID]) {
    set_az = min_az_ms[ID];
  }
  set_el = set_el * ((max_el_ms[ID] - min_el_ms[ID]) / 90)  + min_el_ms[ID];
  if(set_el > max_el_ms[ID]) {
    set_el = max_el_ms[ID];
  }
  if(set_el < min_el_ms[ID]) {
    set_el = min_el_ms[ID];
  }

  az_servos[ID].writeMicroseconds(set_az);
  el_servos[ID].writeMicroseconds(set_el);
}
