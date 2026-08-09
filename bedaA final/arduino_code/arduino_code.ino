/*
 * Displays text sent over the serial port (e.g. from the Serial Monitor) on
 * an attached LCD and sends button press signals to the serial port.
 * YWROBOT
 * Compatible with the Arduino IDE 1.0
 * Library version:1.1
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4); // Set the LCD address to 0x27 for a 20x4 display

// Define button pins
const int button1Pin = 2; // Button 1
const int button2Pin = 3; // Button 2
const int button3Pin = 4; // Button 3

void setup()
{
  // Initialize the LCD
  lcd.init();
  lcd.backlight();

  // Initialize serial communication
  Serial.begin(9600);

  // Set button pins as inputs with internal pull-up resistors
  pinMode(button1Pin, INPUT_PULLUP);
  pinMode(button2Pin, INPUT_PULLUP);
  pinMode(button3Pin, INPUT_PULLUP);
}

void loop()
{
  // Check for serial input to display on the LCD
  if (Serial.available()) {
    delay(100); // Wait a bit for the entire message to arrive
    lcd.clear(); // Clear the LCD
    while (Serial.available() > 0) {
      lcd.write(Serial.read()); // Display each character on the LCD
    }
  }

  // Check button 1 and send a signal
  if (digitalRead(button1Pin) == LOW) { // Button 1 pressed
    Serial.println("button1_pressed");
    delay(300); // Debounce delay
  }

  // Check button 2 and send a signal
  if (digitalRead(button2Pin) == LOW) { // Button 2 pressed
    Serial.println("button2_pressed");
    delay(300); // Debounce delay
  }

  // Check button 3 and send a signal
  if (digitalRead(button3Pin) == LOW) { // Button 3 pressed
    Serial.println("button3_pressed");
    delay(300); // Debounce delay
  }
}
