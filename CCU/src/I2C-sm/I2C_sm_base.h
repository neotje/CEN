#pragma once

#include <Arduino.h>
#include <Wire.h>

#define IS_CONNECTED 0
#define RESTART 1
#define TOGGLE_DEBUG 2
#define SAVE 3
#define LOAD 4

class I2CSensorModuleBase
{
private:
protected:
    int _addr;
    TwoWire *_wire;

    char *_buffer;

    uint8_t _request_to_buffer(int size);
    uint8_t _send_request(int cmd, int size);
    uint8_t _send_request(int cmd, int data, int size);

public:
    I2CSensorModuleBase();
    ~I2CSensorModuleBase();

    int get_addr() { return _addr; }

    bool is_connected();

    void restart()
    {
        _send_request(RESTART, 0);
    }

    void toggle_debug()
    {
        // request module to send debug info over serial.
        _send_request(TOGGLE_DEBUG, 0);
    }

    void save()
    {
        _send_request(SAVE, 0);
    }
    void load()
    {
        _send_request(LOAD, 0);
    }
};