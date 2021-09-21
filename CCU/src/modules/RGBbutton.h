#pragma once

#include <Arduino.h>
#include <ChRt.h>

#include "../config.h"
#include "../thread_priority.h"
#include "../core/core.h"
#include "../serial-UIU/scode.h"

struct RGB
{
    uint8_t r;
    uint8_t g;
    uint8_t b;

    RGB(uint8_t _r = 0, uint8_t _g = 0, uint8_t _b = 0) : r(_r), g(_g), b(_b){};
};

class RGBbutton
{
private:
    static uint8_t pins[4];

    static uint32_t downTime;
    static uint32_t releaseTime;
    static uint32_t pressTime;

    static bool lastState;
    static bool newState;

    static THD_WORKING_AREA(waThread, 128);


public:
    static RGB upColor;
    static RGB downColor;
    static RGB longPressColor;

    static void setup();
    static void loop();

    static THD_FUNCTION(thread, arg);

    static void setColor(uint8_t r = 0, uint8_t g = 0, uint8_t b = 0);
    static void setColor(RGB c)
    {
        setColor(c.r, c.g, c.b);
    }

    static bool isDown();
};

extern event_source_t RGB_BUTTON_EVENT_SRC;
extern RGBbutton rgbButton;
