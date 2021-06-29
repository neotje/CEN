#include "parking.h"

uint8_t ParkingBeeper::beeperPin = BEEPER_PIN;
uint32_t ParkingBeeper::_min = MIN_DISTANCE;
uint32_t ParkingBeeper::_max = MAX_DISTANCE;
bool ParkingBeeper::enable = true;

void ParkingBeeper::loop()
{
    // check if parkingbeeper is enabled and the car is in reverse
    if (enable && ShifterSensor.get_gear() == SHIFTER_SPEEDS - 1)
    {
        
    }
}