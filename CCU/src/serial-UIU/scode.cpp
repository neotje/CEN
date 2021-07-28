#include "scode.h"

SCodeCollection scode;

// define stuff to satisfy the compiler
String SCodeCollection::_line;

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