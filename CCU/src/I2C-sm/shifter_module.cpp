#include "shifter_module.h"

ShifterModule ShifterSensor;

ShifterModule::ShifterModule()
{
    _addr = SHIFTER_ADDRESS;
    _wire = &SHIFTER_WIRE;
}

bool ShifterModule::calibrate(uint8_t gear_num)
{
    _send_request(CMD_SHIFTER_CALIBRATE, gear_num, 1);

    return _buffer[0];
}

int8_t ShifterModule::get_gear()
{
    _request_to_buffer(1);

    return _buffer[0];
}