#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 for a 16 chars and 2 line display
// (If your screen doesn't light up, try 0x3F instead of 0x27)
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int ledPin = 13; // Using the built-in LED for status

void setup() {
  // Initialize serial communication at 9600 baud
  Serial.begin(9600);
  
  // Initialize the LCD
  lcd.init();
  lcd.backlight();
  
  // Print a startup message
  lcd.setCursor(0, 0);
  lcd.print("ice man");
  lcd.setCursor(0, 1);
  lcd.print("Ready...");
  
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Check if data is available from the Python script
  if (Serial.available() > 0) {
    // Flash LED to show data is being received
    digitalWrite(ledPin, HIGH);
    
    // Read the incoming string until a newline character
    String text = Serial.readStringUntil('\n');
    text.trim(); // Clean up any extra spaces
    
    // Clear the screen for the new message
    lcd.clear();
    
    // If the text is longer than 16 characters, we split it across lines
    if (text.length() <= 16) {
      lcd.setCursor(0, 0);
      lcd.print(text);
    } else {
      lcd.setCursor(0, 0);
      lcd.print(text.substring(0, 16));
      lcd.setCursor(0, 1);
      lcd.print(text.substring(16, 32)); // Displays up to 32 characters total
    }
    
    digitalWrite(ledPin, LOW);
  }
}
