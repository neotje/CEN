#include <Arduino.h>
#include <IntervalTimer.h>

#include "core/macros.h"
#include "config.h"

#include "serial-UIU/scode.h"
#include "modules/parking.h"
#include "modules/power.h"

IntervalTimer scodeTimer;

void setup()
{
  Wire2.begin();

  scode.boot();

  TERN_(USE_POWER_MANAGER, power_manager.setup());
  TERN_(USE_PARKING_BEEPER, parking_beeper.setup());

  scodeTimer.begin(scode.loop, 1);
}

void loop()
{
  TERN_(USE_POWER_MANAGER, power_manager.loop());

  if (TERN1(USE_POWER_MANAGER, power_manager.ignition_switch()))
  {
    TERN_(USE_PARKING_BEEPER, parking_beeper.loop());
  }
}