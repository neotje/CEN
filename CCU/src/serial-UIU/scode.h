#pragma once

#include <Arduino.h>
#include <ChRt.h>

#include "../thread_priority.h"
#include "../core/macros.h"
#include "../sensors.h"
#include "../modules/power.h"
#include "../modules/RGBbutton.h"
#include "parser.h"

/*
# Scodes:

## parking sensor
 - S0       - get minimal distance from parking sensors.
 - S1;index - get distance from a parking sensor by index.
 - S2       - get distance report from all sensors.

## shifter sensor
 - S3       - get current gear.


# Mcodes:
 - M0           - save settings / request all sensors to save their configuration.
 - M1           - load settings / request all sensors to load their configuration.
 - M2           - restart everthing.
 - M3;sensor    - get if sensor is online.

## parking beeper
 - M4;enable    - enable/disable the beeper.

## power
 - M5           - check if car ignition is on.
 - M6           - Power cycle all I2C groups
 - M7;int;bool  - Disable/enable group by number.
*/

class SCodeCollection
{
private:
    static String _line;

    static int timed_read();
    static void read_line();

    static THD_WORKING_AREA(waThread, 1000);
    static THD_FUNCTION(thread, arg);

    static THD_WORKING_AREA(waEvtThread, 128);
    static THD_FUNCTION(evtThread, arg);

public:
    static void loop();
    static void switch_case();

    static void sensor_offline()
    {
        CONTROL_PORT.print(parser.command_letter);
        CONTROL_PORT.println(":error:sensor offline");
    }
    static void invalid_input()
    {
        CONTROL_PORT.print(parser.command_letter);
        CONTROL_PORT.println(":error:invalid input");
    }
    static void invalid_arguments()
    {
        CONTROL_PORT.print(parser.command_letter);
        CONTROL_PORT.println(":error:invalid arguments");
    }

    static void report_int(int num)
    {
        CONTROL_PORT.print(parser.command_letter);
        CONTROL_PORT.print(":int:");
        CONTROL_PORT.println(num);
    }

    static void report_bool(bool b)
    {
        CONTROL_PORT.print(parser.command_letter);
        CONTROL_PORT.print(":bool:");
        CONTROL_PORT.println(b);
    }

    static void send_event(String name)
    {
        CONTROL_PORT.print("event:");
        CONTROL_PORT.println(name);
    }

    static void done()
    {
        CONTROL_PORT.println("ready");
    }

    static void setup();

    static void S0();
    static void S1();
    static void S2();
    static void S3();

    static void M0();
    static void M1();
    static void M2();
    static void M3();
    static void M4();

#ifdef USE_POWER_MANAGER
    static void M5();
    static void M6();
    static void M7();
#endif
};

extern SCodeCollection scode;