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

String line1;
String line2;
int scrollDelay = 360;

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

  line1 = String("Temp: " + String(temp) + ", Rad: " + String(ppfd) + " ppfd.");
  line2 = String("RH: " + String(rel_hum) + " %, CO2: " + String(co2) + " ppm.");

  int maxLineLength = max(line1.length(), line2.length());
  int displayTime = maxLineLength * 200; // Adjust the delay multiplier (200) as per your preference

  // Scroll lines vertically on the display
  for (int i = 0; i <= maxLineLength; i++) {
    lcd.setCursor(0, 0);
    lcd.print(line1.substring(i));
    lcd.setCursor(0, 1);
    lcd.print(line2.substring(i));
    delay(scrollDelay);
    lcd.clear();
  }

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

  delay(displayTime);

  lcd.clear();
  delay(100); // Add a small delay before displaying the next values
}
