#pragma once

#include <Arduino.h>
#include <../CEN_BLE/ESP32_BLE_CLIENT.h>
#include "../CEN_BLE/ESP32_BLE_HOST.h"

BLEAdvertisedDevice BLEhost;
BLERemoteService *remoteParkingService = nullptr;
BLERemoteCharacteristic *remoteDistanceCharacteristic = nullptr;

BLEService *parkingService = nullptr;
BLECharacteristic *distanceCharacteristic = nullptr;

void connect()
{
  debugln("Connecting to BLE host...");

  BLEClientTools::setup(BLE_NAME);

  BLEhost = BLEClientTools::searchDeviceByService(PARKING_SERVICE);
  BLEClientTools::connect(&BLEhost);

  remoteParkingService = BLEClientTools::getService(PARKING_SERVICE);
  if (parkingService == nullptr)
    return;

  remoteDistanceCharacteristic = BLEClientTools::getCharacteristic(remoteParkingService, PARKING_CHAR_DISTANCE);
}

void host()
{
  debugln("Starting BLE host...");

  BLEHostTools::setup(BLE_NAME);

  parkingService = BLEHostTools::createService(PARKING_SERVICE);
  distanceCharacteristic = BLEHostTools::createCharacteristic(PARKING_CHAR_DISTANCE, parkingService);
}