#include "RGBbutton.h"

RGBbutton Button1(RGB_BUTTON1_R, RGB_BUTTON1_G, RGB_BUTTON1_B, RGB_BUTTON1_PIN);

void button_evt(uint32_t t)
{}

RGBbutton::RGBbutton(uint8_t r, uint8_t g, uint8_t b, uint8_t pin)
{
    pins[0] = r;
    pins[1] = g;
    pins[2] = b;

    input_pin = pin;

    onPress = &button_evt;
}

RGBbutton::~RGBbutton()
{
}

void RGBbutton::setup()
{
    analogWriteRes(8);

    pinMode(input_pin, INPUT_PULLUP);

    for (size_t i = 0; i < 3; i++)
        pinMode(pins[i], OUTPUT);
}

void RGBbutton::loop()
{
    bool new_state = isDown();

    if(!last_state && new_state)
        downTime = millis();

    if(last_state && !new_state)
    {
        uint32_t t = millis() - downTime;
        onPress(t);
    }

    if (new_state)
    {
        setColor(downColor);
    }
    else
    {
        setColor(upColor);
    }

    last_state = new_state;
}

void RGBbutton::setColor(uint8_t r, uint8_t g, uint8_t b)
{
    analogWrite(pins[2], b);
    analogWrite(pins[1], map(g, 0, 255, 0, 100));
    analogWrite(pins[0], r);
}

bool RGBbutton::isDown()
{
    return !digitalRead(input_pin);
}
