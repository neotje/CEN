#include "parking.h"

uint8_t ParkingBeeper::beeperPin = BEEPER_PIN;
uint32_t ParkingBeeper::_min = MIN_DISTANCE;
uint32_t ParkingBeeper::_max = MAX_DISTANCE;
bool ParkingBeeper::enable = true;
IntervalTimer ParkingBeeper::beeper_timer = IntervalTimer();

void ParkingBeeper::setup()
{
    pinMode(beeperPin, OUTPUT);
}

static bool running = false;

void ParkingBeeper::loop()
{
    // check if parkingbeeper is enabled and the car is in reverse
    if (enable && ShifterSensor.get_gear() == SHIFTER_SPEEDS - 1 && !running)
    {
        
    }
    else
    {
        beeper_timer.end();
    }
}