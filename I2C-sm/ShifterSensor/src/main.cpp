#include <Arduino.h>
#include <Wire.h>
#include "shifter_sensor.h"
#include "../../../CCU/src/config.h"

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

  if (g < SHIFTER_SPEEDS)
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
  case CMD_IS_CONNECTED:
    Wire.write(1);
    break;

  case CMD_RESTART:
    restart();
    break;

  case CMD_TOGGLE_DEBUG:
    debug = !debug;
    break;

  case CMD_SAVE:
    ShifterSensor::save();
    break;

  case CMD_LOAD:
    ShifterSensor::load();
    break;

  case CMD_SHIFTER_CALIBRATE:
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
    case CMD_SHIFTER_CALIBRATE:
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

  Wire.begin(SHIFTER_ADDRESS);
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