#include "power.h"

PowerManager power_manager;

bool PowerManager::_group1_enable = false;
bool PowerManager::_group2_enable = false;
bool PowerManager::_group3_enable = false;
bool PowerManager::_last_ignition_switch_state = false;

void PowerManager::setup()
{
    pinMode(GROUP1_ENABLE_PIN, OUTPUT);
    pinMode(GROUP2_ENABLE_PIN, OUTPUT);
    pinMode(GROUP3_ENABLE_PIN, OUTPUT);
    pinMode(WAKE_RPI_PIN, OUTPUT);

    analogReadResolution(8);
    analogReadAveraging(1);
}

void PowerManager::loop()
{
    bool state = analogRead(VOLTAGE_SENSE1_PIN) > 150;

    if (state != _last_ignition_switch_state)
        _on_ignition_switch(state);

    _last_ignition_switch_state = state;
}

void PowerManager::_on_ignition_switch(bool new_state)
{
    if (new_state)
    {
        wake_rpi();
        scode.send_event("starting");
    }
    else
    {
        scode.send_event("shutdown");
    }

    TERN_(DISABLE_GROUP1_ON_SLEEP, power_manager.set_group(1, new_state));
    TERN_(DISABLE_GROUP2_ON_SLEEP, power_manager.set_group(2, new_state));
    TERN_(DISABLE_GROUP3_ON_SLEEP, power_manager.set_group(3, new_state));
}

bool PowerManager::ignition_switch()
{
    return _last_ignition_switch_state;
}

void PowerManager::wake_rpi()
{
    digitalWriteFast(WAKE_RPI_PIN, HIGH);
    delay(1);
    digitalWriteFast(WAKE_RPI_PIN, LOW);
}

void PowerManager::enable_all_groups()
{
    digitalWriteFast(GROUP1_ENABLE_PIN, HIGH);
    digitalWriteFast(GROUP2_ENABLE_PIN, HIGH);
    digitalWriteFast(GROUP3_ENABLE_PIN, HIGH);

    _group1_enable = true;
    _group2_enable = true;
    _group3_enable = true;
}

void PowerManager::disable_all_groups()
{
    digitalWriteFast(GROUP1_ENABLE_PIN, LOW);
    digitalWriteFast(GROUP2_ENABLE_PIN, LOW);
    digitalWriteFast(GROUP3_ENABLE_PIN, LOW);

    _group1_enable = false;
    _group2_enable = false;
    _group3_enable = false;
}

void PowerManager::set_group(int group, bool enable)
{
    switch (group)
    {
    case 1:
        digitalWriteFast(GROUP1_ENABLE_PIN, enable);
        _group1_enable = enable;
        break;

    case 2:
        digitalWriteFast(GROUP2_ENABLE_PIN, enable);
        _group2_enable = enable;
        break;

    case 3:
        digitalWriteFast(GROUP3_ENABLE_PIN, enable);
        _group3_enable = enable;
        break;

    default:
        break;
    }
}

bool PowerManager::get_group(int group)
{
    switch (group)
    {
    case 1:
        return _group1_enable;

    case 2:
        return _group2_enable;

    case 3:
        return _group3_enable;

    default:
        return false;
    }
}