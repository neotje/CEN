#include "shifter_module.h"

ShifterModule ShifterSensor;

ShifterModule::ShifterModule()
{
    _addr = SHIFTER_ADDR;
    _wire = &Wire2;
}

bool ShifterModule::calibrate(uint8_t gear_num)
{
    _send_request(CALIBRATE, gear_num, 1);

    return _buffer[0];
}

int8_t ShifterModule::get_gear()
{
    _request_to_buffer(1);

    return _buffer[0];
}