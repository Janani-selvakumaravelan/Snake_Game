const int joystickX = A0;  // Analog pin for X-axis
const int joystickY = A1;  // Analog pin for Y-axis
const int buttonPin = 2;   // Digital pin for button

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP); // Set the button pin as input with pull-up resistor
}

void loop() {
  int xValue = analogRead(joystickX);
  int yValue = analogRead(joystickY);
  int buttonState = digitalRead(buttonPin); // Read the button state

  // Send the X, Y values and button state as CSV
  Serial.print(xValue);
  Serial.print(",");
  Serial.print(yValue);
  Serial.print(",");
  Serial.println(buttonState); // Send the button state (0 or 1)

  delay(100); // Adjust the delay as necessary
}
