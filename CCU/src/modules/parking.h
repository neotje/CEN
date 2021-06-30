#pragma once

#include <Arduino.h>
#include <IntervalTimer.h>

#include "../config.h"
#include "../sensors.h"

class ParkingBeeper
{
private:
    static uint8_t beeperPin;
    static uint32_t _max;
    static uint32_t _min;
    static IntervalTimer beeper_timer;

public:
    static bool enable;
    static uint16_t frequency;

    static void setup();
    static void loop();
};

extern ParkingBeeper parking_beeper;