#ifndef shifter_sensor_h
#define shifter_sensor_h

#include <Arduino.h>
#include <EEPROM.h>
#include "../../../CCU/src/config.h"

#define CALIBRATE_MARGIN 25

#define XPORT A0
#define YPORT A1

namespace ShifterSensor
{
    struct Bounds
    {
        int16_t min;
        int16_t max;

        Bounds(int16_t _min, int16_t _max)
        {
            min = _min;
            max = _max;
        };
        Bounds() {};
    };
    struct GearBounds
    {
        // [0]: min
        // [1]: max
        Bounds x;
        Bounds y;

        GearBounds(int16_t xmin, int16_t xmax, int16_t ymin, int16_t ymax) : x(xmin, xmax), y(ymin, ymax) {}
        GearBounds() {};
    };

    bool insideBounds(int16_t x, int16_t y, GearBounds &bounds);

    void readSensor();

    uint16_t getX();
    uint16_t getY();

    int8_t getGear();

    void calibrate();
    void calibrate(int i);

    void save();
    void load();
} // namespace ShifterSensor

#endif