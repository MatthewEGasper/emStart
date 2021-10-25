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
// Must install Servo library to run, see readme
//
////////////////////////////////////////////////////
#include <FeedBackServo.h>
#include <Servo.h>

// define feedback signal pin and servo control pins
#define FEEDBACK_PIN 2
#define AZIMUTH_SERVO_PIN 3
#define ANGLE_SERVO_PIN 4

//define an offset from True North of the Azimuth servo
#define OFFSET_FROM_NORTH 0

// set feedback signal pin number
FeedBackServo azimuth_servo = FeedBackServo(FEEDBACK_PIN);

//set angle servo control pin
Servo angle_servo; 

int azimuth_set = 0;
int angle_set = 0;

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
<<<<<<< Updated upstream
  //set_coord();
  Serial.println("Test");
  delay(1000);
=======
  azimuth_set = Serial.read();
  if (((azimuth_set >= 0)||(azimuth_set <= 360))&&((angle_set >= 0)||(angle_set <= 90)))
  {
    set_coord(azimuth_set,angle_set);
  }
>>>>>>> Stashed changes
}

void set_coord(float azimuth, float angle)
{
  //assumed that North is 0 Degrees
  while((azimuth_servo.Angle() - OFFSET_FROM_NORTH) != azimuth)
  {
    azimuth_servo.rotate((azimuth - OFFSET_FROM_NORTH),1);
  }
  angle_servo.write(angle);

}
