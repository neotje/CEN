#include "RGBbutton.h"

event_source_t RGB_BUTTON_EVENT_SRC;

RGBbutton rgbButton;

uint8_t RGBbutton::pins[4] = {
    RGB_BUTTON1_R,
    RGB_BUTTON1_G,
    RGB_BUTTON1_B,
    RGB_BUTTON1_PIN};

uint32_t RGBbutton::pressTime = 0;
uint32_t RGBbutton::releaseTime = 0;
uint32_t RGBbutton::downTime = 0;

bool RGBbutton::lastState = false;
bool RGBbutton::newState = false;

RGB RGBbutton::downColor;
RGB RGBbutton::upColor;
RGB RGBbutton::longPressColor;

THD_WORKING_AREA(RGBbutton::waThread, 128);
THD_FUNCTION(RGBbutton::thread, arg)
{
    (void)arg;

    upColor = RGB(0, 255, 0);
    downColor = RGB(255, 0, 0);
    longPressColor = RGB(0, 0, 100);

    while (!chThdShouldTerminateX())
    {
        rgbButton.loop();
        chThdSleepMilliseconds(5);
    }
}

void RGBbutton::setup()
{
    analogWriteRes(8);

    pinMode(pins[3], INPUT_PULLUP);

    for (size_t i = 0; i < 3; i++)
        pinMode(pins[i], OUTPUT);

    chThdCreateStatic(&waThread, sizeof(waThread), NORMALPRIO + RGB_BUTTON_PRIO, thread, NULL);
}

void RGBbutton::loop()
{
    newState = isDown();

    if (newState && millis() - pressTime > LONG_PRESS_DURATION)
    {
        setColor(longPressColor);
    }
    else if (newState)
    {
        setColor(downColor);
    }
    else
    {
        setColor(upColor);
    }

    if (!lastState && newState)
        pressTime = millis();

    if (lastState && !newState)
    {
        releaseTime = millis();
        downTime = releaseTime - pressTime;

        if (downTime > LONG_PRESS_DURATION)
        {
            debugln("Button long press.");
            
            chEvtBroadcastFlags(&RGB_BUTTON_EVENT_SRC, RGB_BUTTON_LONG_PRESS_EVT);
        }
        else
        {
            debugln("Button short press.");
            chEvtBroadcastFlags(&RGB_BUTTON_EVENT_SRC, RGB_BUTTON_SHORT_PRESS_EVT);
        }
    }

    lastState = newState;
}

void RGBbutton::setColor(uint8_t r, uint8_t g, uint8_t b)
{
    analogWrite(pins[2], b);
    analogWrite(pins[1], map(g, 0, 255, 0, 100));
    analogWrite(pins[0], r);
}

bool RGBbutton::isDown()
{
    return !digitalRead(pins[3]);
}
