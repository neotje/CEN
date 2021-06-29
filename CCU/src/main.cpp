#include <Arduino.h>

#include "core/macros.h"
#include "config.h"

#include "serial-UIU/scode.h"
#include "modules/parking.h"

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

  TERN_(USE_PARKING_BEEPER, parking_beeper.loop());
}