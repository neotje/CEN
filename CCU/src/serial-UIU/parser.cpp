#include "parser.h"

SCodeParser parser;

// define stuff to satisfy the compiler
String SCodeParser::params[CONTROL_MAX_PARAMS];
char SCodeParser::command_letter;
uint32_t SCodeParser::command_num;
bool SCodeParser::is_valid;

void SCodeParser::reset()
{
    is_valid = false;
    command_letter = 'X';
    command_num = UINT32_MAX;

    for (uint8_t i = 0; i < CONTROL_MAX_PARAMS; i++)
    {
        params[i] = "";
    }
}

void SCodeParser::parse(String &line)
{
    reset();

    line.replace('\r', ' ');
    line.replace('\n', ' ');
    line.trim();

    const unsigned int length = line.length();

    int pos = -1;
    char c;
    String code;

    for (unsigned int i = 0; i < length; i++)
    {
        c = line[i];

        if (c == ';')
        {
            pos++;
            continue;
        }

        if (pos == -1)
            if (i == 0)
                command_letter = toUpperCase(c);
            else
                code.append(c);
        else
            params[pos].append(c);
    }

    command_num = code.toInt();
}