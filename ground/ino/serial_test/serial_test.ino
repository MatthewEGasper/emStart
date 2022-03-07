#include <Servo.h>

void setup() {
  // put your setup code here, to run once:
  Serial1.begin(600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial1.available()) {
    char c = Serial1.read();
    Serial1.write(c);
  }
}
