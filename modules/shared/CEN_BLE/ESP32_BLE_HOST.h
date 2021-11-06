#pragma once

#include <Arduino.h>
#include <BLEDevice.h>

#include "./BLE_CONFIG.h"
#include "../core/debug.h"

namespace BLEHostTools
{
    BLEServer *server = nullptr;
    BLEAdvertising *advertising = nullptr;

    void setup(std::string hostName)
    {
        BLEDevice::init(hostName);

        debugln(BLEDevice::getAddress().toString().c_str());

        server = BLEDevice::createServer();
        advertising = BLEDevice::getAdvertising();
    }

    void addServiceAdvertising(std::string uuid)
    {
        BLEDevice::stopAdvertising();

        advertising->addServiceUUID(uuid);
        advertising->setScanResponse(true);
        advertising->setMinPreferred(0x06);
        advertising->setMinPreferred(0x12);

        BLEDevice::startAdvertising();
    }

    BLEService *createService(std::string uuid)
    {
        BLEUUID serviceUUID(uuid);

        BLEService *service = server->createService(serviceUUID);

        addServiceAdvertising(uuid);

        return service;
    }

    BLECharacteristic *createCharacteristic(std::string uuid, BLEService *service, uint32_t property = BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE | BLECharacteristic::PROPERTY_NOTIFY)
    {
        BLEUUID characteristicUUID(uuid);
        BLECharacteristic *characteristic = service->createCharacteristic(characteristicUUID, property);

        service->start();

        return characteristic;
    }
} // namespace BLEHostTools
