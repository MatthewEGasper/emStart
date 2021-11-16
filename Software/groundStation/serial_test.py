#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.flush()
    
    while True:
        #ser.write(b"azimuth: 23, angle: 27\n")
        #if ser.in_waiting > 0:
        azimuth = 25;
        angle = 34;
        ser.write(str(azimuth).encode('utf-8'))
        ser.write(b"z")
        line = ser.readline().decode('utf-8').rstrip()
        ser.write(str(angle).encode('utf-8'))
        ser.write(b"n")
        print(line)
        time.sleep(1)