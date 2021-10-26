#pragma once

#include <Arduino.h>

class SRO4M
{
private:
    int _triggerPin;
    int _echoPin;
    int _distance;

    void trigger()
    {
        digitalWrite(_triggerPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(_triggerPin, LOW);
    }

public:
    SRO4M(int triggerPin, int echoPin)
    {
        _triggerPin = triggerPin;
        _echoPin = echoPin;
    }
    ~SRO4M() {}

    void begin()
    {
        pinMode(_triggerPin, OUTPUT);
        pinMode(_echoPin, INPUT);
    }

    int measure()
    {
        trigger();

        unsigned long pulseDuration = pulseIn(_echoPin, HIGH);

        _distance = pulseDuration / 58;

        if (_distance < 10 || pulseDuration == 0)
            return 600;

        return _distance;
    }
};