#include <Arduino.h>
#include <Wire.h>

#include "serial-UIU/scode.h"

void setup()
{
  Wire2.begin();

  while (!Serial)
    ;

  scode.boot();
}

void loop()
{
  scode.loop();
}