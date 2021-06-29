#pragma once

#include <Arduino.h>
#include "../config.h"
#include "../sensors.h"

class ParkingBeeper
{
private:
    static uint8_t beeperPin;
    static uint32_t _max;
    static uint32_t _min;
public:
    static bool enable;

    static void loop();
};

extern ParkingBeeper parking_beeper;