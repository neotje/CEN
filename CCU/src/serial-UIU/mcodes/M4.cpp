#include "../scode.h"
#include "../../modules/parking.h"

void SCodeCollection::M4()
{
    if(parser.params[0] == "")
        return invalid_arguments();

    int data = parser.params[0].toInt();
    parking_beeper.enable = data == 1;
    
    done();
}