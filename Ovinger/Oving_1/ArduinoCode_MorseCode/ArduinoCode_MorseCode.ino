
const int green_light_1 = 4;
const int green_light_2 = 7;
const int green_light_3 = 8;
const int red_light = 12;

const int button_pin = 2;
const int T = 150;

int pause_counter = 0;
int symbol_counter = 0;



void setup() {
  Serial.begin(9600);
  pinMode(green_light_1, OUTPUT);
  pinMode(green_light_2, OUTPUT);
  pinMode(green_light_3, OUTPUT);
  pinMode(red_light, OUTPUT);
  pinMode(button_pin, INPUT);
}



// returns true if button is pressed
boolean button_pressed() {
  return digitalRead(button_pin);
}




void handle_signal() {
  symbol_counter = 0;
  while (button_pressed()) {
      delay(T);
      symbol_counter++;
  }
  
  if (symbol_counter > 10) {
    // typed anything wrong? Hold down for at least 10*T
    Serial.print('5');
    return;
  }
  if (symbol_counter > 1) {
    // sends a signal indicating a dash
    Serial.print('2');
    digitalWrite(green_light_1, HIGH);
    digitalWrite(green_light_2, HIGH);
    digitalWrite(green_light_3, HIGH);
    
  } else {
    // sends a signal indicating a dot
    digitalWrite(red_light, HIGH);
    Serial.print('1');  
  }
  handle_pause();
}




void handle_pause() {
  pause_counter = 0;
  while (!button_pressed()) {
      pause_counter++;
      // if the pause_count is higher than 70 we have the end of a word
      if (pause_counter > 70) {
        // sends a signal indicating a end_of_word
        Serial.print('4');
        return;
      }
      delay(T/10);
      // I use T/10 to be able to check for button_pressed more frequently
  }
  // if the pause_count is between 30 and 70, we have the end of a symbol
  if (pause_counter > 30) {
    // sends a signal indicating a end_of_symbol
    Serial.print('3');
    return;
  }

  // if the pause_count is lower than 30, we do nothing
  
}




void loop() {
  if (button_pressed()) {
    // if the button is pressed, we must handle the signal and then the pause
    handle_signal();
    digitalWrite(red_light, LOW);
    digitalWrite(green_light_1, LOW);
    digitalWrite(green_light_2, LOW);
    digitalWrite(green_light_3, LOW);
  }
}


