#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#define LEDPIN 5
#define leeloo 4
// Update these with values suitable for your network.
/*
 * Ceuta
const char* ssid = "MOVISTAR_CAE0";
const char* password = "7RCCCNUb7CCK94734RN9";
const char* mqtt_server = "192.168.1.62";
*/
const char* ssid = "vodafoneAA1520";
const char* password = "PN4HmHsdzeMYRdFC";
const char* mqtt_server = "192.168.0.99";


WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup() {
  pinMode(LEDPIN, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  pinMode(leeloo, OUTPUT);
  float humidity, temp_f;
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
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
  
    if (strcmp(topic,"casa/143/29")==0){
      Serial.print("Encendiendo led habitacion alicia");
      for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
      }
      Serial.println();
    
      // Switch on the LED if an 1 was received as first character
      if ((char)payload[0] == '1') {
        digitalWrite(leeloo, HIGH);   // Turn the LED on (Note that LOW is the voltage level
        // but actually the LED is on; this is because
        // it is acive low on the ESP-01)
      } else {
        digitalWrite(leeloo, LOW);  // Turn the LED off by making the voltage HIGH
      }
    }
}

void reconnect() {
  // Loop until were reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      client.subscribe("casa/143/29");
      //client.subscribe("casa/habitacion/alicia/led");

    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
}
