#include <Arduino.h>

#include "./config.h"
#include "./sensors.h"
#include "./ble.h"
#include "./beeper.h"

const bool hostMode = true;

int *distances;

void setup()
{
#ifdef DEBUG
  Serial.begin(9600);
#endif

  if (hostMode)
  {
    host();
  }
  else
  {
    connect();
  }

  setupBeeper();
  setupSensors();
}

void loop()
{
  distances = measureAllSensors();

  int d = distances[0];
  for(size_t i = 0; i < SENSOR_COUNT; i++) {
    if(distances[i] > 10 && distances[i] < d) {
      d = distances[i];
    }
  }

  smallestDistance = d;

  if (hostMode)
  {
    sendDistancesToCharacteristic(distances, distanceCharacteristic);
    BLEDevice::startAdvertising();
  }
  else
  {
    sendDistancesToCharacteristic(distances, remoteDistanceCharacteristic);

    if (!BLEClientTools::isConnected() || distanceCharacteristic == nullptr)
    {
      connect();
    }
  }
}
