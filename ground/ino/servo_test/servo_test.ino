#include <Servo.h>

Servo s[4];

int ms = 0;
int min_val = 900;
int max_val = 1900;

void setup() {
  float avg;
  avg = (2390 - 615) / 2;
  avg += 615;
//  s[0].attach(22);
  s[1].attach(23);
//  s[2].attach(24);
  s[3].attach(25);
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
