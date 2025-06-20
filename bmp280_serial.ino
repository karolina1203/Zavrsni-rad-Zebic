#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp; // koristi I2C

void setup() {
  Serial.begin(115200);
  while (!Serial); // čekaj dok se serijska ne pokrene

  if (!bmp.begin()) {
    Serial.println("BMP280 nije pronađen!");
    while (1);
  }
}

void loop() {
  float pressure = bmp.readPressure() / 100.0F; // pretvori u hPa (hektopaskale)
  Serial.println(pressure); // šalji kao tekst na Serial (jedan broj po liniji)
  delay(1000); // 1 Hz frekvencija
}
