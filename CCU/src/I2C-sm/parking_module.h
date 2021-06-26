#ifndef parking_module_h
#define parking_module_h

#include "I2C_sm_base.h"

#define PARKING_ADDR 2
#define GET_DISTANCE 3

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

ParkingModule::ParkingModule()
{
    _addr = PARKING_ADDR;
    _wire = &Wire2;
}

int32_t ParkingModule::get_distance(uint8_t i)
{
    _wire->beginTransmission(_addr);
    _wire->write(GET_DISTANCE);
    _wire->write(i);
    _wire->endTransmission();

    _request_to_buffer(4);

    memcpy(&_distance, _buffer, 4);
    return _distance;
}

int32_t ParkingModule::get_min_distance()
{
    _request_to_buffer(4);
    memcpy(&_distance, _buffer, 4);
    
    return _distance;
}

#endif