int pir_pin = 2;
int led_pin = 3;

void setup() 
{
  pinMode(pir_pin, INPUT);
  pinMode(led_pin, OUTPUT);
  Serial.begin(9600);
}
void loop() 
{
  if(digitalRead(pir_pin) == HIGH)
  {
    digitalWrite(led_pin, HIGH);
    Serial.println("¡Intrusos!");
  }
  else
  {
    digitalWrite(led_pin, LOW);
    Serial.println("Modo vigilante");
  }
}
