#include <Arduino.h>
#include <Wire.h>
#include "../../../CCU/src/config.h"

#define SENSORS 4

uint8_t pins[SENSORS][2] = {
    {3, 4},
    {5, 6},
    {7, 8},
    {9, 10}};

int32_t distances[SENSORS];

int cmd;
bool debug = false;
int _buffer_size = 0;

uint8_t *_buffer;

int64_t duration;

int32_t distance;

void restart()
{
  pinMode(DD2, OUTPUT);
  digitalWrite(DD2, HIGH);
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

  case CMD_PARKING_GET_DISTANCE:
    int32_t resp;
    if (_buffer[0] >= SENSORS)
    {
      resp = -1;
    }
    else
    {
      resp = distances[_buffer[0]];
    }

    delete[] _buffer;
    _buffer = new uint8_t[4];
    memcpy(_buffer, &resp, 4);

    Wire.write(_buffer, 4);
    break;

  default:
    distance = INT32_MAX;

    for (uint8_t i = 0; i < SENSORS; i++)
    {
      distance = min(distance, distances[i]);
    }

    delete[] _buffer;
    _buffer = new uint8_t[4];
    memcpy(_buffer, &distance, 4);
    Wire.write(_buffer, 4);
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
    delete[] _buffer;
    _buffer = new uint8_t[size - 1];
    Wire.readBytes(_buffer, size - 1);
  }
}

void setup()
{
  Serial.begin(9600);
  Serial.println("Booting...");

  for (int i = 0; i < SENSORS; i++)
  {
    pinMode(pins[i][0], OUTPUT);
    pinMode(pins[i][1], INPUT);
  }

  Wire.begin(PARKING_ADDRESS);
  Wire.onRequest(requestEvent);
  Wire.onReceive(recieveEvent);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
}

void trigger(uint8_t pin)
{
  digitalWrite(pin, LOW);
  delayMicroseconds(2);
  digitalWrite(pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pin, LOW);
}

void loop()
{
  for (int8_t i = 0; i < SENSORS; i++)
  {
    trigger(pins[i][0]);

    duration = pulseIn(pins[i][1], HIGH);

    distances[i] = duration * 0.034 / 2;
  }

  if (debug)
  {
    for (int i = 0; i < SENSORS; i++)
    {
      Serial.print("Sensor ");
      Serial.print(i);
      Serial.print(": ");
      Serial.println(distances[i]);
    }
    Serial.println();
  }

  //delay(10);
}