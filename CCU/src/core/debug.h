#pragma once

#include "../config.h"

#ifdef DEBUG
    #define debug(x) Serial.print(x)
    #define debugln(x) Serial.print("DEBUG:");Serial.println(x)
#else
    #define debug(x)
    #define debugln(x)
#endif