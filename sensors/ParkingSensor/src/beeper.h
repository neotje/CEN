#pragma once

#include <Arduino.h>
#include <EasyBuzzer.h>
#include "./config.h"

TaskHandle_t beeperTask;

bool enableBeeper = true;
int smallestDistance = 300;

void oneBeep(uint32_t duration, double freq)
{
    ledcWriteTone(0, freq);
    delay(duration);
    ledcWrite(0, 0);
}

void beeperTaskHandler(void *param)
{
    for (;;)
    {
        if (smallestDistance < 25)
        {
            ledcWriteTone(0, BUZZER_TONE);
            while (smallestDistance < 25)
            {
                vTaskDelay(1);
            };
        }
        else if (smallestDistance <= 300)
        {
            oneBeep(BEEP_DURATION, BUZZER_TONE);

            unsigned long start = millis();
            while (millis() - start < map(smallestDistance, 30, 300, BEEP_DURATION / 2, BEEPER_MAX_INTERVAL)) {
                vTaskDelay(1);
            };
        }
        else
        {
            ledcWrite(0, 0);
        }

        vTaskDelay(1);
    }
}

void setupBeeper()
{
    ledcSetup(0, 5000, 8);
    ledcAttachPin(BUZZER_PIN, 0);

    xTaskCreatePinnedToCore(
        beeperTaskHandler,
        "BeeperTask",
        10000,
        NULL,
        0,
        &beeperTask,
        0);
}