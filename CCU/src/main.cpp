#include <Arduino.h>
#include <Snooze.h>
#include <ChRt.h>

#include "core/core.h"
#include "config.h"
#include "thread_priority.h"

#include "serial-UIU/scode.h"
#include "modules/parking.h"
#include "modules/power.h"
#include "modules/RGBbutton.h"

void setupThread()
{
  TERN_(USE_START_BUTTON, rgbButton.setup());
  TERN_(USE_POWER_MANAGER, powerManager.setup());
  TERN_(USE_SCODE, scode.setup());
}

void setup()
{
  // initialize events.
  TERN_(USE_START_BUTTON, chEvtObjectInit(&RGB_BUTTON_EVENT_SRC));
  TERN_(USE_POWER_MANAGER, chEvtObjectInit(&POWER_MANAGER_EVENT_SRC));

  // start system and setup threads.
  chBegin(setupThread);

  while (true)
  {
  }
}

void loop()
{
  chThdSleepMilliseconds(1000);
}