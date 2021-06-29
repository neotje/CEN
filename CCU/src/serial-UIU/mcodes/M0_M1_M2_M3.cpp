#include "../scode.h"

// - M0         - save settings / request all sensors to save their configuration.
void SCodeCollection::M0()
{
    ShifterSensor.save();
    ParkingSensor.save();

    done();
}

// - M1         - load settings / request all sensors to load their configuration.
void SCodeCollection::M1() 
{
    ShifterSensor.load();
    ParkingSensor.load();

    done();
}

// - M2         - restart everthing.
void SCodeCollection::M2()
{
    ShifterSensor.restart();
    ParkingSensor.restart();

    boot();
}

// - M3;sensor  - get if sensor is online.
void SCodeCollection::M3()
{
    if(parser.params[0] == "")
        return invalid_arguments();

    if(parser.params[0] == "ParkingSensor")
        report_int(ParkingSensor.is_connected());
    if(parser.params[0] == "ShifterSensor")
        report_int(ShifterSensor.is_connected());
    
    done();
}