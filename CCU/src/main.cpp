#include <Arduino.h>
#include <IntervalTimer.h>

#include "core/macros.h"
#include "config.h"

#include "serial-UIU/scode.h"
#include "modules/parking.h"

IntervalTimer scodeTimer;

void setup()
{
  Wire2.begin();

  scode.boot();

  TERN_(USE_PARKING_BEEPER, parking_beeper.setup());

  scodeTimer.begin(scode.loop, 1);
}

void loop()
{
  //scode.loop();

  TERN_(USE_PARKING_BEEPER, parking_beeper.loop());
}