#pragma once

#include <BLEDevice.h>
#include "./config.h"
#include "./SRO4M.h"
#include "../core/debug.h"

SRO4M sensors[SENSOR_COUNT] = {
    SRO4M(13, 26),
    SRO4M(12, 25),
    SRO4M(14, 33),
    SRO4M(27, 32)};

int measuredDistances[SENSOR_COUNT];

void setupSensors()
{
    for (size_t i = 0; i < SENSOR_COUNT; i++)
        sensors[i].begin();
}

int *measureAllSensors() {
    for(size_t i = 0; i < SENSOR_COUNT; i++)
    {
        measuredDistances[i] = sensors[i].measure();
        delay(10);
    }

    return measuredDistances;
}

void sendDistancesToCharacteristic(int *distances, BLERemoteCharacteristic *characteristic)
{
    String msg = "";

    for (size_t i = 0; i < SENSOR_COUNT; i++)
    {
        msg += String(distances[i]);

        if(i < SENSOR_COUNT - 1)
            msg += ",";
    }
    
    debugln(msg);
    characteristic->writeValue(msg.c_str());
}

void sendDistancesToCharacteristic(int *distances, BLECharacteristic *characteristic)
{
    String msg = "";

    for (size_t i = 0; i < SENSOR_COUNT; i++)
    {
        msg += String(distances[i]);

        if(i < SENSOR_COUNT - 1)
            msg += ",";
    }
    
    debugln(msg);
    characteristic->setValue(msg.c_str());
    characteristic->notify();
}