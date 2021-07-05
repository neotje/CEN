#pragma once
#include <Arduino.h>

/*
Modules
*/

// power manager
#define USE_POWER_MANAGER
#define DISABLE_GROUP1_ON_SLEEP
#define DISABLE_GROUP2_ON_SLEEP
#define DISABLE_GROUP3_ON_SLEEP

// parking
//#define USE_PARKING_BEEPER
#define MIN_DISTANCE 20
#define MAX_DISTANCE 1000



/*
Pins

Reserved:
 - 9  (D7/RX2)
 - 10 (D8/TX2)
 - 16 (D24/SCL2)
 - 17 (D25/SDA2)
 - 36 (D14/TX3)
 - 37 (D15/RX3)
 - 38 (D16/SCL1)
 - 39 (D17/SDA1)
 - 40 (D18/SDA)
 - 41 (D19/SCL)
*/
#define GROUP1_ENABLE_PIN 2         // 2
#define GROUP2_ENABLE_PIN 3         // 3
#define GROUP3_ENABLE_PIN 4         // 4

#define BEEPER_PIN 5                // 5

// uses mosfet to short GPIO3 to GND to wake up pi
#define WAKE_RPI_PIN 6              // 6

#define VOLTAGE_SENSE1_PIN A17      // 41
#define VOLTAGE_SENSE2_PIN A16      // 40



/*
Serial controls
*/
#define CONTROL_PORT          Serial
#define CONTROL_DEBUG

#define CONTROL_SEPERATOR     ';'
#define CONTROL_TERMINATOR    '\n'
#define CONTROL_MAX_PARAMS    6



/*
      I2C sensor modules
*/

#define I2C_GROUP1 Wire
#define I2C_GROUP2 Wire1
#define I2C_GROUP3 Wire2

// base
#define CMD_IS_CONNECTED            0
#define CMD_RESTART                 1
#define CMD_TOGGLE_DEBUG            2
#define CMD_SAVE                    3
#define CMD_LOAD                    4

// parking module
#define PARKING_WIRE I2C_GROUP3
#define PARKING_ADDRESS             0
#define CMD_PARKING_GET_DISTANCE    3

// shifter_module
#define SHIFTER_WIRE I2C_GROUP3
#define SHIFTER_ADDRESS             1
#define SHIFTER_SPEEDS              7
#define CMD_SHIFTER_CALIBRATE       5
