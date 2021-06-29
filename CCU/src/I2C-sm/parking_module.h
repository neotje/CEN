#pragma once

#include "I2C_sm_base.h"

class ParkingModule : public I2CSensorModuleBase
{
private:
    int32_t _distance;

public:
    ParkingModule();
    ~ParkingModule() {}

    int32_t get_distance(uint8_t i);
    int32_t get_min_distance();
};

extern ParkingModule ParkingSensor;