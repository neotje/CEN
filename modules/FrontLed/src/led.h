#pragma once

#include <Arduino.h>
#include <FastLED.h>

#include "./config.h"
#include "ble.h"

CRGB *leftLeds;
CRGB *rightLeds;

class LeftStripCallback : public BLECharacteristicCallbacks
{
    void onWrite(BLECharacteristic *pCharacteristic)
    {
        int start = micros();
        debugln(pCharacteristic->getValue().c_str());

        const std::string value = pCharacteristic->getValue();

        std::string indexStr = value.substr(0, 2);
        std::string hexStr = value.substr(2, 9);

        int i = atoi(indexStr.c_str());
        int c = (int)strtol(hexStr.c_str(), NULL, 0);

        debugln(i);
        debugln(c);

        leftLeds[i].setColorCode(c);

        FastLED.show();
        debugln(micros() - start);
    }
};

class RightStripCallback : public BLECharacteristicCallbacks
{
    void onWrite(BLECharacteristic *pCharacteristic)
    {
        debugln(pCharacteristic->getValue().c_str());

        const std::string value = pCharacteristic->getValue();

        std::string indexStr = value.substr(0, 2);
        std::string hexStr = value.substr(2, 9);

        int i = atoi(indexStr.c_str());
        int c = (int)strtol(hexStr.c_str(), NULL, 0);

        debugln(i);
        debugln(c);

        rightLeds[i].setColorCode(c);

        FastLED.show();
    }
};

class FillStripsCallback : public BLECharacteristicCallbacks
{
    void onWrite(BLECharacteristic *pCharacteristic)
    {
        debugln(pCharacteristic->getValue().c_str());

        const std::string value = pCharacteristic->getValue();

        int color = (int)strtol(value.c_str(), NULL, 0);

        FastLED.showColor(CRGB(color));
    }
};

void setupLeds(int ledsPerSide)
{
    leftLeds = new CRGB[ledsPerSide];
    rightLeds = new CRGB[ledsPerSide];

    FastLED.addLeds<WS2813, DATA_PIN_LEFT, RGB>(leftLeds, ledsPerSide);
    FastLED.addLeds<WS2813, DATA_PIN_RIGHT, RGB>(rightLeds, ledsPerSide);

    FastLED.clear(true);

    leftStripService->setCallbacks(new LeftStripCallback());
    rightStripService->setCallbacks(new RightStripCallback());
    fillStripsService->setCallbacks(new FillStripsCallback());
}

void ledFadeIn(CRGB color, int duration)
{
    int time = 0;
    int start = millis();

    while (millis() - start < duration)
    {
        time = millis() - start;

        float progress = float(time) / float(duration);
        FastLED.showColor(color, progress * 256);
    }
}

void ledFadeOut(CRGB color, int duration)
{
    int time = 0;
    int start = millis();

    while (millis() - start < duration)
    {
        time = millis() - start;

        float progress = float(time) / float(duration);
        FastLED.showColor(color, (1.0 - progress) * 256);
    }

    FastLED.clear(true);
}