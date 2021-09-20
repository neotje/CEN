#include "scode.h"

SCodeCollection scode;

// define stuff to satisfy the compiler
String SCodeCollection::_line;

THD_WORKING_AREA(SCodeCollection::waThread, 1000);
THD_WORKING_AREA(SCodeCollection::waEvtThread, 128);

void SCodeCollection::setup()
{
    CONTROL_PORT.begin(9600);
    CONTROL_PORT.println("boot:Teensy Car");
    parser.reset();

    chThdCreateStatic(waEvtThread, sizeof(waEvtThread), NORMALPRIO + SCODE_EVT_PRIO, evtThread, NULL);
    chThdCreateStatic(waThread, sizeof(waThread), NORMALPRIO + SCODE_PRIO, thread, NULL);
}

THD_FUNCTION(SCodeCollection::thread, arg)
{
    (void)arg;

    done();

    while (!chThdShouldTerminateX())
    {
        loop();
        chThdYield();
    }
}

THD_FUNCTION(SCodeCollection::evtThread, arg)
{
  (void)arg;

  event_listener_t rgbButtonListener;
  event_listener_t powerManagerListener;

  chEvtRegisterMask(&RGB_BUTTON_EVENT_SRC, &rgbButtonListener, EVENT_MASK(0));
  chEvtRegisterMask(&POWER_MANAGER_EVENT_SRC, &powerManagerListener, EVENT_MASK(1));

  while (!chThdShouldTerminateX())
  {
    eventmask_t evt = chEvtWaitAny(ALL_EVENTS);

    if (evt & EVENT_MASK(0))
    {
      eventflags_t flag = chEvtGetAndClearFlags(&rgbButtonListener);

      if (flag & RGB_BUTTON_SHORT_PRESS_EVT)
      {
        send_event("button_short_press");
      }
      if (flag & RGB_BUTTON_LONG_PRESS_EVT)
      {
        send_event("button_long_press");
      }
    }
    if (evt & EVENT_MASK(1))
    {
      eventflags_t flag = chEvtGetAndClearFlags(&powerManagerListener);

      if (flag & IGNITION_ON_EVENT)
      {
        send_event("ignition_on");
      }
      if (flag & IGNITION_OFF_EVENT)
      {
        send_event("ignition_off");
      }
    }

    chThdYield();
  }
}


int SCodeCollection::timed_read()
{
    int c;
    unsigned long startMillis = millis();
    do
    {
        c = CONTROL_PORT.read();
        if (c >= 0)
            return c;
        yield();
    } while (millis() - startMillis < 1000);
    return -1; // -1 indicates timeout
}

void SCodeCollection::loop()
{
    if (CONTROL_PORT.available() > 0)
    {
        int c = CONTROL_PORT.read();

        if (c < 0)
            return;

#ifdef CONTROL_DEBUG
        CONTROL_PORT.print((char)c);
#endif

        if (c == 0)
            return;

        if (c == CONTROL_TERMINATOR)
        {
            switch_case();
            _line = "";
        }

        if (c == 8)
            _line.remove(_line.length() - 1);
        else
            _line += (char)c;
    }
}

void SCodeCollection::switch_case()
{
    parser.parse(_line);

    switch (parser.command_letter)
    {
    case 'S':
        switch (parser.command_num)
        {
        case 0:
            S0();
            break;

        case 1:
            S1();
            break;

        case 2:
            S2();
            break;

        case 3:
            S3();
            break;

        default:
            break;
        }
        break;

    case 'M':
        switch (parser.command_num)
        {
            CODE(0, M0)

            CODE(1, M1)

            CODE(2, M2)

            CODE(3, M3)

            CODE(4, M4)

#ifdef USE_POWER_MANAGER
            CODE(5, M5)

            CODE(6, M6)

            CODE(7, M7)
#endif

        default:
            break;
        }
        break;

    default:
        break;
    }

    parser.reset();
}