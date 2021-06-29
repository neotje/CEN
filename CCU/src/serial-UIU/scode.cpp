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
        int c = timed_read();

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
        case 0:
            M0();
            break;

        case 1:
            M1();
            break;

        case 2:
            M2();
            break;

        case 3:
            M3();
            break;

        default:
            break;
        }
        break;

    default:
        break;
    }

    parser.reset();
}