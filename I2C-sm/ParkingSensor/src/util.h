#ifndef util_h
#define util_h

#include <Arduino.h>

static bool loopDelay(uint32_t msec)
{
    static int32_t to_go = INT32_MAX;
    static bool result = false;
    static uint32_t start = micros();

    if(result)
        result = !result;

    if (msec < to_go)
        to_go = msec;

    if (micros() - start >= 1000)
    {
        if(--to_go <= 0)
            result = true;
        start += 1000;
    }

    return result;
}

#endif