#include "../scode.h"

void SCodeCollection::S3()
{
    if (!ShifterSensor.is_connected())
        return sensor_offline();

    report_int(ShifterSensor.get_gear());
    done();
}