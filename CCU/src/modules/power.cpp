#include "power.h"

event_source_t POWER_MANAGER_EVENT_SRC;

PowerManager powerManager;

bool PowerManager::_group1Enable = false;
bool PowerManager::_group2Enable = false;
bool PowerManager::_group3Enable = false;
bool PowerManager::_lastIgnitionSwitchState = true;

thread_t *PowerManager::shutdownThreadPointer;

void PowerManager::setup()
{
    pinMode(GROUP1_ENABLE_PIN, OUTPUT);
    pinMode(GROUP2_ENABLE_PIN, OUTPUT);
    pinMode(GROUP3_ENABLE_PIN, OUTPUT);
    pinMode(RPI_GLOBAL_EN_PIN, OUTPUT);
    pinMode(FAN_AUDIO_MOSFET_PIN, OUTPUT);

    analogReadResolution(8);
    analogReadAveraging(1);

    chThdCreateStatic(waThread, sizeof(waThread), NORMALPRIO + POWER_MANAGER_PRIO, thread, NULL);
}

THD_WORKING_AREA(PowerManager::waThread, 128);
THD_FUNCTION(PowerManager::thread, arg)
{
    (void)arg;

    while (!chThdShouldTerminateX())
    {
        loop();
        chThdSleepMilliseconds(1000);
    }
}

THD_WORKING_AREA(PowerManager::waShutdownThread, 128);
THD_FUNCTION(PowerManager::shutdownThread, arg)
{
    (void)arg;

    for (size_t i = 0; i < 60; i++)
    {
        chThdSleepSeconds(1);

        scode.send_event("shutdown_now");

        if (chThdShouldTerminateX())
        {
            chThdExit(0);
            break;
        }
    }

    if (!chThdShouldTerminateX())
        digitalWriteFast(RPI_GLOBAL_EN_PIN, HIGH);

    chThdExit(0);
}

void PowerManager::loop()
{
    bool state = analogRead(VOLTAGE_SENSE1_PIN) > 150;

    if (state != _lastIgnitionSwitchState)
        _onIgnitionSwitch(state);

    _lastIgnitionSwitchState = state;
}

void PowerManager::_onIgnitionSwitch(bool new_state)
{
    if (new_state)
    {
        turnOnAudioFans();
        turnOnRPI();
        chEvtBroadcastFlags(&POWER_MANAGER_EVENT_SRC, IGNITION_ON_EVENT);
    }
    else
    {
        chEvtBroadcastFlags(&POWER_MANAGER_EVENT_SRC, IGNITION_OFF_EVENT);
        turnOffRPI();
        turnOffAudioFans();
    }

    TERN_(DISABLE_GROUP1_ON_SLEEP, powerManager.setGroup(1, new_state));
    TERN_(DISABLE_GROUP2_ON_SLEEP, powerManager.setGroup(2, new_state));
    TERN_(DISABLE_GROUP3_ON_SLEEP, powerManager.setGroup(3, new_state));
}

bool PowerManager::isIgnitionSwitch()
{
    return _lastIgnitionSwitchState;
}

void PowerManager::enableAllGroups()
{
    digitalWriteFast(GROUP1_ENABLE_PIN, HIGH);
    digitalWriteFast(GROUP2_ENABLE_PIN, HIGH);
    digitalWriteFast(GROUP3_ENABLE_PIN, HIGH);

    _group1Enable = true;
    _group2Enable = true;
    _group3Enable = true;
}

void PowerManager::disableAllGroups()
{
    digitalWriteFast(GROUP1_ENABLE_PIN, LOW);
    digitalWriteFast(GROUP2_ENABLE_PIN, LOW);
    digitalWriteFast(GROUP3_ENABLE_PIN, LOW);

    _group1Enable = false;
    _group2Enable = false;
    _group3Enable = false;
}

void PowerManager::setGroup(int group, bool enable)
{
    switch (group)
    {
    case 1:
        digitalWriteFast(GROUP1_ENABLE_PIN, enable);
        _group1Enable = enable;
        break;

    case 2:
        digitalWriteFast(GROUP2_ENABLE_PIN, enable);
        _group2Enable = enable;
        break;

    case 3:
        digitalWriteFast(GROUP3_ENABLE_PIN, enable);
        _group3Enable = enable;
        break;

    default:
        break;
    }
}

bool PowerManager::getGroup(int group)
{
    switch (group)
    {
    case 1:
        return _group1Enable;

    case 2:
        return _group2Enable;

    case 3:
        return _group3Enable;

    default:
        return false;
    }
}

void PowerManager::turnOffRPI()
{
    shutdownThreadPointer = chThdCreateStatic(waShutdownThread, sizeof(waShutdownThread), NORMALPRIO + 6, shutdownThread, NULL);
}
void PowerManager::turnOnRPI()
{
    chThdTerminate(shutdownThreadPointer);
    digitalWriteFast(RPI_GLOBAL_EN_PIN, LOW);
}

void PowerManager::turnOnAudioFans()
{
    digitalWriteFast(FAN_AUDIO_MOSFET_PIN, HIGH);
}
void PowerManager::turnOffAudioFans()
{
    digitalWriteFast(FAN_AUDIO_MOSFET_PIN, LOW);
}