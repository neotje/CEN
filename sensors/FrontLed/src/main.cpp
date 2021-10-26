#include <Arduino.h>
#include <FastLED.h>

#include "config.h"
#include "led.h"
#include "ble.h"

void setup()
{
#ifdef DEBUG
  Serial.begin(9600);
#endif

  startBleHost(BLE_HOST_NAME);

  setupLeds(LED_COUNT_PER_SIDE);

  ledFadeIn(CRGB::White, 4000);
  ledFadeOut(CRGB::White, 1000);
}

void loop()
{
  // put your main code here, to run repeatedly:
}