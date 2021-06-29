#pragma once

/*
Serial controls
*/
#define CONTROL_PORT Serial

#define CONTROL_SEPERATOR ';'
#define CONTROL_TERMINATOR '\n'
#define CONTROL_MAX_PARAMS 6

//#define USE_PARKING_BEEPER
#define BEEPER_PIN 2
#define MIN_DISTANCE 20
#define MAX_DISTANCE 1000


/*
      I2C sensor modules
*/
// base
#define CMD_IS_CONNECTED 0
#define CMD_RESTART      1
#define CMD_TOGGLE_DEBUG 2
#define CMD_SAVE         3
#define CMD_LOAD         4

// parking module
#define PARKING_ADDRESS 0
#define CMD_PARKING_GET_DISTANCE 5

// shifter_module
#define SHIFTER_ADDRESS 1
#define SHIFTER_SPEEDS 7
#define CMD_SHIFTER_CALIBRATE 5
