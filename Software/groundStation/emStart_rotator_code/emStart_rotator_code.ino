////////////////////////////////////////////////////
//                  _____ _             _   
//                 / ____| |           | |  
//   ___ _ __ ___ | (___ | |_ __ _ _ __| |_ 
//  / _ \ '_ ` _ \ \___ \| __/ _` | '__| __|
// |  __/ | | | | |____) | || (_| | |  | |_ 
//  \___|_| |_| |_|_____/ \__\__,_|_|   \__|
//
////////////////////////////////////////////////////
// School:        Embry-Riddle Daytona Beach
// Engineer:      Matthew Grabasch
//
// Create Date:   10/4/2021
// Design Name:   emStart_rotator_code.ino
// Project Name:  emStart 
// Tool Versions: Arduino 1.8.16
// Description:   
//
//
// Revision:      1.0
// Revision 1.0 - Base functionallity Completed with 
// serial communication and servo movement
//
// Additional Comments:
// Must install Servo library to run, see readme
//
////////////////////////////////////////////////////
#include <FeedBackServo.h>
#include <Servo.h>

// define feedback signal pin and servo control pins
#define FEEDBACK_PIN 2
#define AZIMUTH_SERVO_PIN 6
#define ANGLE_SERVO_PIN 5

//Defines offsets so 0-90/0-360 values can operate though the system
#define AZIMUTH_OFFSET 56
#define ANGLE_OFFSET 58

//define an offset from True North of the Azimuth servo
#define OFFSET_FROM_NORTH 0

// set feedback signal pin number
FeedBackServo azimuth_servo = FeedBackServo(FEEDBACK_PIN);

//set angle servo control pin
Servo angle_servo; 

//set initial location for each servo
int azimuth_set = 0;
int angle_set = 0;

//initial set for "single run" provision for setting servos
int azimuth_old = 1000;
int angle_old = 1000;

//counter to eliminate startup issues with serial transmission
int run_cnt = 0;

void setup() {
    // set servo control pin number
    azimuth_servo.setServoControl(AZIMUTH_SERVO_PIN);
    
    // set Kp to proportional controller
    azimuth_servo.setKp(1.0);

    //atatch servo to control pin
    angle_servo.attach(ANGLE_SERVO_PIN);
    
    Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  String az_ser = "";
  String an_ser = "";
  if (Serial.available() > 0) {
    
    //ending on RPI to ensure separation of 2 values
    az_ser = Serial.readStringUntil('z');
    an_ser = Serial.readStringUntil('n');
    
    //convert vaues from Serial port to int
    azimuth_set = az_ser.toInt();
    angle_set = an_ser.toInt();

    //prints results to be seen on serial bus
    Serial.print("Azimuth: ");
    Serial.print(azimuth_set);
    Serial.print("\n");
    Serial.print("Angle: ");
    Serial.print(angle_set);
    Serial.print("\n");

    //startup protection issue handling
    run_cnt++;
  }

 
  if (run_cnt >= 3)
  {
    if (((azimuth_set >= 0)&&(azimuth_set <= 360))&&((angle_set >= 0)&&(angle_set <= 90)))
    {
      if ((azimuth_set != azimuth_old) || (angle_set != angle_old))
      {
        //run the set fucntion
        set_coord(azimuth_set,angle_set);
        Serial.print("I Ran\n");
        azimuth_old = azimuth_set;
        angle_old = angle_set;
      }
    }
  }
  
}

void set_coord(int azimuth, int angle)
{
  //helps to fix some servo jitter
  delay(100);
  
  //assumed that North is 0 Degrees, sets both servo positions
  azimuth_servo.rotate((azimuth+AZIMUTH_OFFSET+OFFSET_FROM_NORTH),1);
  angle_servo.write(angle+ANGLE_OFFSET);
}
