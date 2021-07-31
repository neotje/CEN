#pragma once

#include <Arduino.h>

#include "../config.h"
#include "../serial-UIU/scode.h"

struct RGB
{
    uint8_t r;
    uint8_t g;
    uint8_t b;

    RGB(uint8_t _r = 0, uint8_t _g = 0, uint8_t _b = 0): r(_r), g(_g), b(_b) {};
};

class RGBbutton
{
private:
    uint8_t pins[3];
    uint8_t input_pin;

    uint32_t downTime = 0;

    bool last_state = false;

public:
    RGBbutton(uint8_t r, uint8_t g, uint8_t b, uint8_t pin);
    ~RGBbutton();

    RGB upColor;
    RGB downColor;
    void (*onPress)(uint32_t);

    void setup();
    void loop();

    void setColor(uint8_t r = 0, uint8_t g = 0, uint8_t b = 0);
    void setColor(RGB c)
    {
        setColor(c.r, c.g, c.b);
    }

    bool isDown();
};

extern RGBbutton Button1;