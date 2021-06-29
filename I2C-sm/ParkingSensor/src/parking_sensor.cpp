#include "parking_sensor.h"

uint32_t DISTANCE_FUNC() {
    return 0;
}

ParkingSensor::ParkingSensor(uint8_t buzzerPin, uint32_t maximumDistance, uint32_t minimalDistance, uint32_t maxTimeBetweenBeeps)
{
    maxDistance = maximumDistance;
    minDistance = minimalDistance;
    maxInterval = maxTimeBetweenBeeps;

    _distance = maxDistance;
    _interval = maxInterval;

    _frequency = 1000;
    _beepDuration = 300;

    _enable = true;

    _buzzer = buzzerPin;

    _distance_f = DISTANCE_FUNC;

    pinMode(_buzzer, OUTPUT);
}

void ParkingSensor::loop()
{
    if (_enable)
    {
        _distance = _distance_f();

        Serial.println(_distance);

        _distance = max(minDistance, min(_distance, maxDistance));
        
        _interval = map(_distance, minDistance, maxDistance, 0, maxInterval);

        /* if(loopDelay(_interval + _beepDuration - 10))
            tone(_buzzer, _frequency, _beepDuration); */

        delay(_interval + _beepDuration - 10);
        tone(_buzzer, _frequency, _beepDuration + 250);
    }
}