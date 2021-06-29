#ifndef parking_sensor_h
#define parking_sensor_h

#include <Arduino.h>
#include "util.h"

class ParkingSensor
{
private:
    uint32_t _distance;
    uint32_t _interval;

    uint32_t _frequency;
    uint32_t _beepDuration;

    uint8_t _buzzer;

    bool _enable;

    uint32_t (*_distance_f)();

    void drawDistance();

public:
    uint32_t maxDistance;
    uint32_t minDistance;
    uint32_t maxInterval;

    ParkingSensor(uint8_t buzzerPin, uint32_t maximumDistance = 200, uint32_t minimalDistance = 20, uint32_t maxTimeBetweenBeeps = 1000);
    ~ParkingSensor() {}

    uint32_t getInterval()
    {
        return _interval;
    }

    uint32_t getDistance()
    {
        return _distance;
    }

    void disable() {
        _enable = false;
    }

    void enable() {
        _enable = true;
    }

    bool isEnabled() {
        return _enable;
    }

    void setDistanceFunction(uint32_t (*funct)())
    {
        _distance_f = funct;
    }

    void setDistance(uint32_t distance)
    {
        _distance = distance;
    }

    void loop();
};

#endif