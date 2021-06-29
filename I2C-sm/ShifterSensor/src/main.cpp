#include <Arduino.h>
#include <Wire.h>
#include "shifter_sensor.h"

#define ADDR 1

#define IS_CONNECTED 0
#define RESTART 1
#define TOGGLE_DEBUG 2
#define SAVE 3
#define LOAD 4
#define CALIBRATE 5

int cmd;
bool debug = false;

int _buffer_size = 0;
uint8_t *_buffer;

void restart()
{
  pinMode(DD2, OUTPUT);
  digitalWrite(DD2, HIGH);
}

void requestCalibrate()
{
  uint8_t g = _buffer[0];

  if (debug)
  {
    Serial.print("Calibrating gear: ");
    Serial.println(g);
  }

  if (g < GEARS)
  {
    ShifterSensor::calibrate(g);
    Wire.write(1);
    return;
  }
  Wire.write(0);
}

void requestEvent()
{
  if (debug)
    Serial.println("Request");

  switch (cmd)
  {
  case IS_CONNECTED:
    Wire.write(1);
    break;

  case RESTART:
    restart();
    break;

  case TOGGLE_DEBUG:
    debug = !debug;
    break;

  case SAVE:
    ShifterSensor::save();
    break;

  case LOAD:
    ShifterSensor::load();
    break;

  case CALIBRATE:
    requestCalibrate();
    break;

  default:
    Wire.write(ShifterSensor::getGear());
  }
  cmd = -1;
}

void recieveEvent(int size)
{
  cmd = Wire.read();

  if (debug)
  {
    Serial.print("recieved: ");
    Serial.println(cmd);
  }

  if (size > 1)
  {
    _buffer = new uint8_t[size - 1];
    switch (cmd)
    {
    case CALIBRATE:
      _buffer[0] = Wire.read();
      break;

    default:
      break;
    }
  }
}

void setup()
{
  Serial.begin(9600);
  Serial.println("Booting...");

  Wire.begin(ADDR);
  Wire.onRequest(requestEvent);
  Wire.onReceive(recieveEvent);

  ShifterSensor::load();

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
}

void loop()
{
  if (debug)
  {
    Serial.print(" X: ");
    Serial.print(ShifterSensor::getX());
    Serial.print(" Y: ");
    Serial.print(ShifterSensor::getY());
    Serial.print(" G: ");
    Serial.println(ShifterSensor::getGear());
  }
  delay(1000);
}