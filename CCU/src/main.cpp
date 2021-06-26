#include <Arduino.h>

#include "car.h"

void setup()
{
  Serial2.begin(115200);

  pinMode(LED_BUILTIN, OUTPUT);

  Wire2.begin();

  while (!Serial)
    ;

  Serial.print("Shifter sensor connected: ");
  Serial.println(Shifter.is_connected());
  Serial.print("Parking sensor connected: ");
  Serial.println(ParkingSensor.is_connected());

  digitalWrite(LED_BUILTIN, HIGH);

  /* for (int i = 0; i < GEARS; i++)
  {
    Serial.print("gear: ");
    Serial.println(i);

    Shifter.calibrate(i);

    delay(3000);
  }

  Shifter.save(); */
  
}

void loop()
{
  Serial.println(ParkingSensor.get_distance(0));
  //delay(1);
  Serial.println(ParkingSensor.get_distance(1));
  //delay(1);
  Serial.println(ParkingSensor.get_distance(2));
  //delay(1);
  Serial.println(ParkingSensor.get_distance(3));
  //delay(1);
  Serial.println(ParkingSensor.get_min_distance());
  Serial.println();
  Serial.println(Shifter.get_gear());
  Serial.println();
  Serial.println();
  delay(1000);
}