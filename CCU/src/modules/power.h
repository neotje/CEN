#pragma once

#include <Arduino.h>
#include <Snooze.h>

#include "../config.h"
#include "../core/macros.h"
#include "../serial-UIU/scode.h"

class PowerManager
{
private:
    static bool _group1_enable;
    static bool _group2_enable;
    static bool _group3_enable;

    static bool _last_ignition_switch_state;

    static void _on_ignition_switch(bool new_state);

public:
    static void setup();
    static void loop();

    static bool ignition_switch();

    static void wake_rpi();

    /*
    I2C groups power managements
    */
    static void enable_all_groups();
    static void disable_all_groups();
    static void set_group(int group, bool enable);
    static bool get_group(int group);
};

extern PowerManager power_manager;