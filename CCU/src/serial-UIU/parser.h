#pragma once

#include <Arduino.h>

#include "../config.h"

class SCodeParser
{
public:
    static String params[CONTROL_MAX_PARAMS];

    static char command_letter;
    static uint32_t command_num;
    static bool is_valid;

    static void reset();

    static void parse(String &line);
};

extern SCodeParser parser;
