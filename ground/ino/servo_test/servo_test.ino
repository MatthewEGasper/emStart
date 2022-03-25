#include <Servo.h>

Servo s[4];

int ms = 0;
int min_val = 550;
int max_val = 2390;

void setup() {
  float avg;
  avg = (2390 - 615) / 2;
  avg += 615;
  s[0].attach(50);
//  s[1].attach(51);
//  s[2].attach(52);
//  s[3].attach(53);
}

void loop() {
  for(ms = min_val; ms < max_val; ms++) {
    for(int i=0; i<4; i++) {
      s[i].writeMicroseconds(ms);
    }
    delay(5);
  }
  for(ms = max_val; ms > min_val; ms--) {
    for(int i=0; i<4; i++) {
      s[i].writeMicroseconds(ms);
    }
    delay(5);
  }
}
