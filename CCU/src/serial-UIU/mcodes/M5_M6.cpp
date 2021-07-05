#include "../scode.h"
#include "../../modules/power.h"

#ifdef USE_POWER_MANAGER

// - M5           - check if car ignition is on.
void SCodeCollection::M5()
{
    report_bool(power_manager.ignition_switch());
    done();
}

// - M6           - Power cycle all I2C groups
void SCodeCollection::M6()
{
    power_manager.disable_all_groups();
    power_manager.enable_all_groups();
    done();
}

#endif