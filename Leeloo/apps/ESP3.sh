#!/bin/bash
mkdir -p apps/ESP3

echo '#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#define LEDPIN 5
#define leeloo 4
int base = LOW; 
const char* ssid = "<wifi>";
const char* password = "<contraseña>";
const char* mqtt_server = "<ip_broker>";


WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup() {
  pinMode(LEDPIN, OUTPUT);
  pinMode(leeloo, INPUT);
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {

  delay(20);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(400);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando realizar conexión MQTT...");
    if (client.connect("ESP8266Client")) {
      Serial.println("conectado");
    } else {
      Serial.println(" reintentando en 5 segundos");
      delay(4000);
    }
  }
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  movimiento = digitalRead(leeloo);
  if (movimiento == HIGH)   //si está activado
   { 
      if (base == LOW)  //si previamente estaba apagado
      {
        Serial.println("Sensor activado");
        client.publish("casa/'$1'/'$2'", "1", payload);
        base = HIGH;
      }
   }
   {
      if (base == HIGH)
      {
        Serial.println("Sensor parado");
        base = LOW;
      }
   }
}' > apps/ESP3/ESP3.ino
