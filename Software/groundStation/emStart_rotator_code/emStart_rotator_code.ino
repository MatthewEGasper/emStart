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
// Revision:      0.0
// Revision 0.0 - File Created
//
// Additional Comments:
//
////////////////////////////////////////////////////
#include <FeedBackServo.h>
#include <Servo.h>

// define feedback signal pin and servo control pins
#define FEEDBACK_PIN 2
#define AZIMUTH_SERVO_PIN 3
#define ANGLE_SERVO_PIN 4

// set feedback signal pin number
FeedBackServo azimuth_servo = FeedBackServo(FEEDBACK_PIN);

//set angle servo control pin
Servo angle_servo; 

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
  //set_coord();
}

void set_coord(float azimuth, float angle)
{
  //assumed that North is 0 Degrees
  azimuth_servo.rotate(azimuth,1);

  angle_servo.write(angle);

}
