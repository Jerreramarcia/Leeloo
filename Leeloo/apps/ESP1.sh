#!/bin/bash
mkdir -p apps/ESP1

echo '#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#define LEDPIN 5
#define leeloo 4
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
  pinMode(leeloo, OUTPUT);
  float humidity, temp_f;
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {

  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
    if (strcmp(topic,"casa/'$1'/'$2'")==0){
      Serial.print("Encendiendo led habitacion alicia");
      for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
      }
      Serial.println();
        if ((char)payload[0] == '\'1\'') {
        digitalWrite(leeloo, HIGH);   
        // but actually the LED is on; this is because
        // it is acive low on the ESP-01)
      } else {
        digitalWrite(leeloo, LOW);  
      }
    }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando realizar conexión MQTT...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      client.subscribe("casa/'$1'/'$2'");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" reintentando en 5 segundos");
      delay(5000);
    }
  }
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
}' > apps/ESP1/ESP1.ino
