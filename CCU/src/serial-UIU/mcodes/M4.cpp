#include "../scode.h"
#include "../../modules/parking.h"

// - M4;enable    - enable/disable the beeper.
void SCodeCollection::M4()
{
    if(parser.params[0] == "")
        return invalid_arguments();

    int data = parser.params[0].toInt();
    parking_beeper.enable = data == 1;
    
    done();
}