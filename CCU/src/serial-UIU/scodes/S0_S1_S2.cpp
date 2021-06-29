#include "../scode.h"

// - S0       - get minimal distance from parking sensors.
void SCodeCollection::S0()
{
    if (!ParkingSensor.is_connected())
        return sensor_offline();

    report_int(ParkingSensor.get_min_distance());
    done();
}

// - S1;index - get distance from a parking sensor by index.
void SCodeCollection::S1()
{
    if (!ParkingSensor.is_connected())
        return sensor_offline();

    if (parser.params[0] == "")
        return invalid_arguments();

    report_int(ParkingSensor.get_distance(parser.params[0].toInt()));
    done();
}

// - S2       - get distance report from all sensors.
void SCodeCollection::S2()
{
    if (!ParkingSensor.is_connected())
        return sensor_offline();

    for (int i = 0; i < 4; i++)
        report_int(ParkingSensor.get_distance(i));

    done();
}