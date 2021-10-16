#include <Arduino.h>
#include <CEN_BLE/ESP32_BLE_CLIENT.h>

#include "./config.h"
#include "./sensors.h"
#include "./ble.h"

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

  setupSensors();
}

void loop()
{
  distances = measureAllSensors();

  if (hostMode)
  {
    sendDistancesToCharacteristic(distances, distanceCharacteristic);
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
