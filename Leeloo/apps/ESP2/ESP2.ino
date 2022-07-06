#include <ESP8266WiFi.h>
#include <PubSubClient.h>
const char* ssid = "vodafoneAA1520";
const char* password = "PN4HmHsdzeMYRdFC";
const char* mqtt_server = "192.168.0.99";
#include <DHT.h>
#define DHTTYPE DHT11
#define DHTPIN 2

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup() {
  float humidity, temp_f;
  Serial.begin(115200);
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


  Serial.println("WiFi conectado");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando realizar conexión MQTT...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
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
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  String payload = String(t).c_str() + "_" + String(t).c_str();
  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    client.publish("casa/143/30", String(t).c_str(), payload);
  }
}
