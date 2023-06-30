// LCD: GND, Positive, A4, A5
// T-RH: GND, Positive, A3
// Lighting: GND(Red), GND(Black),Positive(Yellow),A0(Green)
// CO2: GND, Vin, A1

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTTYPE    DHT11     // DHT 11
#define DHTPIN A3
DHT_Unified dht(DHTPIN, DHTTYPE);

float temp = 0;
float rel_hum = 0;
int PARsensorPin = A0, CO2sensorPin = A1;
float ppfdsensorValue = 0, ppfd = 0;
float CO2sensorValue = 0, co2 = 0;

LiquidCrystal_I2C lcd(0x27, 16, 2); // set the LCD address to 0x27 for a 16 chars and 2 line display

void setup() {
  Serial.begin(9600); // Start serial communication
  lcd.init();
  lcd.backlight();
  dht.begin();
}

void loop() {
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  temp = event.temperature;
  dht.humidity().getEvent(&event);
  rel_hum = event.relative_humidity;

  ppfdsensorValue = analogRead(PARsensorPin);
  ppfd = (ppfdsensorValue / 1023.0) * (5.0 * 417.7);
  CO2sensorValue = analogRead(CO2sensorPin);
  co2 = CO2sensorValue * 5.0 / 1023 * 500;

  lcd.setCursor(0, 0);
  lcd.print(temp, 2);
  lcd.print("C");
  lcd.print(co2, 2);
  lcd.print("ppm");

  lcd.setCursor(0, 1);
  lcd.print(rel_hum, 2);
  lcd.print("%");
  lcd.print(ppfd, 2);
  lcd.print("ppfd;");


  // Send the measured data over serial communication
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.print(" C, Relative Humidity: ");
  Serial.print(rel_hum);
  Serial.print(" %, PAR: ");
  Serial.print(ppfd);
  Serial.print(" ppfd, CO2: ");
  Serial.print(co2);
  Serial.println(" ppm");

  delay(5000); // Delay between readings and display updates
  lcd.clear();
}
