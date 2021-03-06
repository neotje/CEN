#pragma once

#include <Arduino.h>
#include <Snooze.h>
#include <ChRt.h>

#include "../config.h"
#include "../core/core.h"
#include "../serial-UIU/scode.h"
#include "RGBbutton.h"

extern event_source_t POWER_MANAGER_EVENT_SRC;

class PowerManager
{
private:
    static bool _group1Enable;
    static bool _group2Enable;
    static bool _group3Enable;

    static bool _lastIgnitionSwitchState;

    static bool _rpiEnabled;
    static bool _audioFansEnabled;

    static bool _goToSleep;

    static void _onIgnitionSwitch(bool newState);

    static THD_WORKING_AREA(waThread, 128);
    static THD_FUNCTION(thread, arg);

    static THD_WORKING_AREA(waEventThread, 128);
    static THD_FUNCTION(eventThread, arg);
    static thread_t *shutdownThreadPointer;

public:
    static void setup();
    static void loop();

    static bool isIgnitionSwitch();

    /*
    I2C groups power managements
    */
    static void enableAllGroups();
    static void disableAllGroups();
    static void setGroup(int group, bool enable);
    static bool getGroup(int group);

    /*
    RPI4 power controls
    */
    static void turnOnRPI();
    static void turnOffRPI();

    /*
   other system controls
   */
    static void turnOnAudioFans();
    static void turnOffAudioFans();

    static void goToSleep();
};

extern PowerManager powerManager;