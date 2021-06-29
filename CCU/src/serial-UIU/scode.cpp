#include "scode.h"

SCodeCollection scode;

// define stuff to satisfy the compiler
String SCodeCollection::_line;

void SCodeCollection::loop()
{
    if (CONTROL_PORT.available() > 0)
    {
        _line = CONTROL_PORT.readStringUntil(CONTROL_TERMINATOR);

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
}