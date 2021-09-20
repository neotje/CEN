#include <Arduino.h>
#include <IntervalTimer.h>
#include <ChRt.h>

#include "core/macros.h"
#include "config.h"
#include "thread_priority.h"
#include "events.h"

#include "serial-UIU/scode.h"
#include "modules/parking.h"
#include "modules/power.h"
#include "modules/RGBbutton.h"

static THD_WORKING_AREA(waRgbButtonThread, 128);
static THD_FUNCTION(rgbButtonThread, arg)
{
  (void)arg;

  rgbButton1.setup();
  rgbButton1.upColor = RGB(0, 255, 0);
  rgbButton1.downColor = RGB(255, 0, 0);

  while (!chThdShouldTerminateX())
  {
    rgbButton1.loop();
    chThdSleepMilliseconds(5);
  }
}

void setupThread()
{
  TERN_(USE_START_BUTTON, chThdCreateStatic(waRgbButtonThread, sizeof(waRgbButtonThread), NORMALPRIO + RGB_BUTTON_PRIO, rgbButtonThread, NULL));

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