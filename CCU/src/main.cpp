#include <Arduino.h>
#include <IntervalTimer.h>

#include "core/macros.h"
#include "config.h"

#include "serial-UIU/scode.h"
#include "modules/parking.h"
#include "modules/power.h"
#include "modules/RGBbutton.h"

IntervalTimer scodeTimer;

void setup()
{
  I2C_GROUP1.begin();
  I2C_GROUP2.begin();
  I2C_GROUP3.begin();

  TERN_(USE_POWER_MANAGER, power_manager.setup());
  TERN_(USE_PARKING_BEEPER, parking_beeper.setup());
  TERN_(USE_START_BUTTON, Button1.setup());

  scode.boot();
  scodeTimer.begin(scode.loop, 1);

  Button1.upColor = RGB(0, 255, 0);
  Button1.downColor = RGB(255, 0, 0);
}

void loop()
{
  TERN_(USE_POWER_MANAGER, power_manager.loop());
  TERN_(USE_START_BUTTON, Button1.loop());

  if (TERN1(USE_POWER_MANAGER, power_manager.ignition_switch()))
  {
    TERN_(USE_PARKING_BEEPER, parking_beeper.loop());
  }
}