#include "parking_module.h"

ParkingModule ParkingSensor;

ParkingModule::ParkingModule()
{
    _addr = PARKING_ADDRESS;
    _wire = &PARKING_WIRE;
}

int32_t ParkingModule::get_distance(uint8_t i)
{
    _wire->beginTransmission(_addr);
    _wire->write(CMD_PARKING_GET_DISTANCE);
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