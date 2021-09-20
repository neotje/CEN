#include "../scode.h"
#include "../../modules/power.h"

#ifdef USE_POWER_MANAGER

// - M5           - check if car ignition is on.
void SCodeCollection::M5()
{
    report_bool(powerManager.isIgnitionSwitch());
    done();
}

// - M6           - Power cycle all I2C groups
void SCodeCollection::M6()
{
    powerManager.disableAllGroups();
    powerManager.enableAllGroups();
    done();
}

// - M7;int;bool  - Disable/enable group by number.
void SCodeCollection::M7()
{
    if (parser.params[0] == "" || parser.params[1] == "")
        return invalid_arguments();

    int group = parser.params[0].toInt();
    bool state = parser.params[1].toInt();

    if (group > 3 || group < 1)
        return invalid_input();

    powerManager.setGroup(group, state);
    done();
}

#endif