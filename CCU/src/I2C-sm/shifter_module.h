#ifndef shifter_module_h
#define shifter_module_h

#include "I2C_sm_base.h"

#define GEARS 7

#define SHIFTER_ADDR 1

#define SAVE 3
#define LOAD 4
#define CALIBRATE 5

struct Bounds
{
    int16_t min;
    int16_t max;

    Bounds(int16_t _min, int16_t _max)
    {
        min = _min;
        max = _max;
    };
    Bounds(){};
};
struct GearBounds
{
    // [0]: min
    // [1]: max
    Bounds x;
    Bounds y;

    GearBounds(int16_t xmin, int16_t xmax, int16_t ymin, int16_t ymax) : x(xmin, xmax), y(ymin, ymax) {}
    GearBounds(){};
};

class ShifterModule : public I2CSensorModuleBase
{
private:
    GearBounds _gears[GEARS];

public:
    ShifterModule();
    ~ShifterModule() {}

    void save(){
        _send_request(SAVE, 0);
    }
    void load(){
        _send_request(LOAD, 0);
    }

    int8_t get_gear();

    /* 
    gear 0 = neutral
    last gear = reverse
    */
    bool calibrate(uint8_t gear_num);
};

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

#endif