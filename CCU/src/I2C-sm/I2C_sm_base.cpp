#include "I2C_sm_base.h"

I2CSensorModuleBase::I2CSensorModuleBase()
{
}

I2CSensorModuleBase::~I2CSensorModuleBase()
{
}

uint8_t I2CSensorModuleBase::_request_to_buffer(int size)
{
    // request data
    delete[] _buffer;
    _buffer = new char[size];
    _wire->requestFrom(_addr, size);

    if (size == 0)
        return 0;

    _wire->readBytes(_buffer, size);
    return size;
}

uint8_t I2CSensorModuleBase::_send_request(int cmd, int size)
{
    // send command
    _wire->beginTransmission(_addr);
    _wire->write(cmd);
    _wire->endTransmission();

    return _request_to_buffer(size);
}

uint8_t I2CSensorModuleBase::_send_request(int cmd, int data, int size)
{
    // send command
    _wire->beginTransmission(_addr);
    _wire->write(cmd);
    _wire->write(data);
    _wire->endTransmission();

    return _request_to_buffer(size);
}

bool I2CSensorModuleBase::is_connected()
{
    _wire->beginTransmission(_addr);
    _wire->write(IS_CONNECTED);
    _wire->endTransmission();

    _wire->requestFrom(_addr, 1);

    uint32_t start = micros();
    uint32_t timout = 100 * 1000;

    while (_wire->available() == 0)
    {
        if (micros() - start >= timout)
        {
            return false;
        }
    }

    return _wire->read() == 1;
}