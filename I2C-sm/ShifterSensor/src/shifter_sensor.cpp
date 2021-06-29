#include "shifter_sensor.h"

ShifterSensor::GearBounds gears[GEARS];

uint16_t x;
uint16_t y;

bool ShifterSensor::insideBounds(int16_t x, int16_t y, GearBounds &bounds)
{
    return x > bounds.x.min && x < bounds.x.max && y > bounds.y.min && y < bounds.y.max;
}

void ShifterSensor::readSensor()
{
    x = analogRead(XPORT);
    y = analogRead(YPORT);
}

int8_t ShifterSensor::getGear()
{
    readSensor();

    for (int8_t i = 0; i < GEARS; i++)
    {
        if (insideBounds(x, y, gears[i]))
            return i;
    }
    return -1;
}

uint16_t ShifterSensor::getX() { return x; }
uint16_t ShifterSensor::getY() { return y; }

void ShifterSensor::calibrate()
{
    for (int i = 0; i < GEARS; i++)
    {
        Serial.print("move into gear: ");
        Serial.println(i);
        delay(3000);

        calibrate(i);
    }
}

void ShifterSensor::calibrate(int i)
{
    readSensor();
    gears[i] = GearBounds(x - CALIBRATE_MARGIN, x + CALIBRATE_MARGIN, y - CALIBRATE_MARGIN, y + CALIBRATE_MARGIN);
}

void ShifterSensor::save()
{
    //int size = GEARS * 4 * 2;
    EEPROM.put(0, gears);
}

void ShifterSensor::load()
{
    EEPROM.get(0, gears);
}