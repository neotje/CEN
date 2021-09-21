#include "power.h"

event_source_t POWER_MANAGER_EVENT_SRC;

PowerManager powerManager;

bool PowerManager::_group1Enable = false;
bool PowerManager::_group2Enable = false;
bool PowerManager::_group3Enable = false;
bool PowerManager::_lastIgnitionSwitchState = false;
bool PowerManager::_rpiEnabled = false;
bool PowerManager::_audioFansEnabled = false;
bool PowerManager::_goToSleep = false;

SnoozeCompare compare;
SnoozeDigital digital;
SnoozeUSBSerial usbSerial;
SnoozeBlock config(usbSerial, compare, digital);

thread_t *PowerManager::shutdownThreadPointer;

void PowerManager::setup()
{
    pinMode(GROUP1_ENABLE_PIN, OUTPUT);
    pinMode(GROUP2_ENABLE_PIN, OUTPUT);
    pinMode(GROUP3_ENABLE_PIN, OUTPUT);
    pinMode(RPI_GLOBAL_EN_PIN, OUTPUT);
    pinMode(FAN_AUDIO_MOSFET_PIN, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);

    analogReadResolution(8);
    analogReadAveraging(1);

    digital.pinMode(RGB_BUTTON1_PIN, INPUT_PULLUP, FALLING);
    compare.pinMode(VOLTAGE_SENSE3_PIN, HIGH, 0.5);

    turnOffRPI();
    turnOffAudioFans();

    chThdCreateStatic(waEventThread, sizeof(waEventThread), NORMALPRIO + POWER_MANAGER_EVT_PRIO, eventThread, NULL);
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

THD_WORKING_AREA(PowerManager::waEventThread, 128);
THD_FUNCTION(PowerManager::eventThread, arg)
{
    (void)arg;

    event_listener_t listener;
    event_listener_t buttonListener;

    chEvtRegisterMask(&POWER_MANAGER_EVENT_SRC, &listener, EVENT_MASK(0));
    chEvtRegisterMask(&RGB_BUTTON_EVENT_SRC, &buttonListener, EVENT_MASK(1));

    eventmask_t evt;
    eventflags_t flag;

    while (!chThdShouldTerminateX())
    {
        evt = chEvtWaitAny(ALL_EVENTS);

        if (evt & EVENT_MASK(0))
        {
            flag = chEvtGetAndClearFlags(&listener);

            if (flag & IGNITION_OFF_EVENT)
            {
                debugln("Starting shutdown process.");

                turnOffAudioFans();
                disableAllGroups();

                for (size_t i = 0; i < RPI_SHUTDOWN_DURATION; i++)
                {
                    debugln(i);

                    evt = chEvtWaitAnyTimeout(ALL_EVENTS, TIME_S2I(1));
                    flag = chEvtGetAndClearFlags(&listener);

                    if (flag & IGNITION_ON_EVENT)
                    {
                        debugln("Ignition back on canceling shutdown process.");
                        break;
                    }
                }

                if (evt == 0)
                {
                    turnOffRPI();
                    goToSleep();
                }
            }
            if (flag & IGNITION_ON_EVENT)
            {
                turnOnAudioFans();
                turnOnRPI();
                enableAllGroups();
            }
        }

        if (evt & EVENT_MASK(1))
        {
            flag = chEvtGetAndClearFlags(&buttonListener);

            if (flag & RGB_BUTTON_LONG_PRESS_EVT)
            {
                if (!_rpiEnabled)
                {
                    turnOnAudioFans();
                    turnOnRPI();
                }
                else
                {
                    turnOffRPI();
                    turnOffAudioFans();
                    goToSleep();
                }
            }
        }
    }
}

void PowerManager::loop()
{
    bool state = analogRead(VOLTAGE_SENSE3_PIN) > 30;

    if (state != _lastIgnitionSwitchState)
        _onIgnitionSwitch(state);

    _lastIgnitionSwitchState = state;
}

void PowerManager::_onIgnitionSwitch(bool new_state)
{
    if (new_state)
    {
        debugln("Ignition on.");
        chEvtBroadcastFlags(&POWER_MANAGER_EVENT_SRC, IGNITION_ON_EVENT);
    }
    else
    {
        debugln("Ignition off.");
        chEvtBroadcastFlags(&POWER_MANAGER_EVENT_SRC, IGNITION_OFF_EVENT);
    }
}

void PowerManager::goToSleep()
{
    debugln("Going to sleep.");

    chSysLock();
    int who = Snooze.sleep(config);
    chSysUnlock();

    turnOnAudioFans();
    turnOnRPI();
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

void PowerManager::turnOnRPI()
{
    debugln("Turning on RPI.");
    digitalWriteFast(RPI_GLOBAL_EN_PIN, HIGH);
    _rpiEnabled = true;
}
void PowerManager::turnOffRPI()
{
    debugln("Turning off RPI.");
    digitalWriteFast(RPI_GLOBAL_EN_PIN, LOW);
    _rpiEnabled = false;
}

void PowerManager::turnOnAudioFans()
{
    debugln("Turning on AMP and Fans.");
    digitalWriteFast(FAN_AUDIO_MOSFET_PIN, HIGH);
    _audioFansEnabled = true;
}
void PowerManager::turnOffAudioFans()
{
    debugln("Turning off AMP and Fans.");
    digitalWriteFast(FAN_AUDIO_MOSFET_PIN, LOW);
    _audioFansEnabled = false;
}