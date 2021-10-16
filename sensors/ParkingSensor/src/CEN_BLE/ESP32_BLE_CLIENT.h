#pragma once

#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEClient.h>

#include "./BLE_CONFIG.h"
#include "../core/debug.h"

namespace BLEClientTools
{
    BLEScan *scanner = nullptr;
    BLEClient *client = nullptr;
    BLEAdvertisedDevice *connectedDevice = nullptr;

    void setup(std::string clientName)
    {
        if(BLEDevice::getInitialized()) BLEDevice::deinit(true);
        
        BLEDevice::init(clientName);
        BLEDevice::startAdvertising();

        scanner = BLEDevice::getScan();
        client = BLEDevice::createClient();
    }

    BLEScanResults scan(uint32_t duration = 2)
    {
        scanner->clearResults();

        scanner->setInterval(1349);
        scanner->setWindow(449);
        scanner->setActiveScan(true);
        scanner->start(duration, false);

        BLEScanResults scanResults = scanner->getResults();

        debugln("BLE Scanner found:");
        for (size_t i = 0; i < scanResults.getCount(); i++)
        {
            debugln(scanResults.getDevice(i).toString().c_str());
        }

        return scanResults;
    }

    BLEAdvertisedDevice searchDeviceByService(std::string serviceUUID)
    {
        BLEUUID uuid(serviceUUID);

        BLEScanResults scanResults = scan();

        BLEAdvertisedDevice device;

        for (size_t i = 0; i < scanResults.getCount(); i++)
        {
            device = scanResults.getDevice(i);

            if (device.haveServiceUUID() && device.isAdvertisingService(uuid))
            {
                debugln("BLE found device with service UUID:");
                debugln(serviceUUID.c_str());

                return device;
            }
        }
    }

    bool isConnected()
    {
        return client->isConnected();
    }

    bool connect(BLEAdvertisedDevice *device)
    {
        debug("DEBUG:");
        debug("Connecting to: ");
        debug(device->getAddress().toString().c_str());
        debug("\n");

        client->connect(device);

        if (isConnected())
        {
            connectedDevice = device;
            return true;
        }
        else
        {
            connectedDevice = nullptr;
            return false;
        }
    }

    void disconnect()
    {
        debug("DEBUG:");
        debug("Disconnecting from: ");
        debug(client->getPeerAddress().toString().c_str());
        debug("\n");

        client->disconnect();
    }

    BLERemoteService *getService(std::string uuid)
    {
        if (!isConnected())
            return nullptr;

        BLEUUID serviceUUID(uuid);

        BLERemoteService *service = client->getService(serviceUUID);

        if (service == nullptr)
        {
            debug("DEBUG:");
            debug("Failed to find service: ");
            debug(uuid.c_str());
            debug("\n");

            disconnect();
        }

        debug("DEBUG:");
        debug("Found service: ");
        debug(uuid.c_str());
        debug("\n");

        return service;
    }

    BLERemoteCharacteristic *getCharacteristic(BLERemoteService *service, std::string uuid)
    {
        if(service == nullptr)
            return nullptr;

        BLEUUID characteristicUUID(uuid);

        BLERemoteCharacteristic *characteristic = service->getCharacteristic(characteristicUUID);

        if (characteristic == nullptr)
        {
            debug("DEBUG:");
            debug("Failed to find characteristic: ");
            debug(uuid.c_str());
            debug("\n");

            disconnect();
        }

        debug("DEBUG:");
        debug("Found characteristic: ");
        debug(uuid.c_str());
        debug("\n");

        return characteristic;
    }
} // namespace BLE