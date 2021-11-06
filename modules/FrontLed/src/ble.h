#pragma once

#include <Arduino.h>

#include "../CEN_BLE/ESP32_BLE_HOST.h"

BLEService *ledStripService = nullptr;
BLECharacteristic *leftStripService = nullptr;
BLECharacteristic *rightStripService = nullptr;
BLECharacteristic *fillStripsService = nullptr;

class ServerCallbacks : public BLEServerCallbacks
{
    void onConnect(BLEServer *pServer)
    {
        pServer->startAdvertising();
    }
};

void startBleHost(std::string hostName)
{
    debugln("Starting ble host");

    BLEHostTools::setup(hostName);

    BLEHostTools::server->setCallbacks(new ServerCallbacks());

    ledStripService = BLEHostTools::createService(LED_STRIP_SERVICE);
    leftStripService = BLEHostTools::createCharacteristic(LEFT_STRIP_CHARACTERISTIC, ledStripService);
    rightStripService = BLEHostTools::createCharacteristic(RIGHT_STRIP_CHARACTERISTIC, ledStripService);
    fillStripsService = BLEHostTools::createCharacteristic(FILL_STRIPS_CHARACTERISTIC, ledStripService);
}