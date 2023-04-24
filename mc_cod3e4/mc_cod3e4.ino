/*
 *  Author : Craig Doyle
 *  Date : 24/03/23
 *  Description : A simple program for ESP32 devices to send and recieve analogue signals through MQTT or Serial connections
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>

/*
 *  DEFINITIONS
 */
#define APin 3
#define OutMode 1
#define BUILTIN_LED 0
/*
 * Output Mode ^
 * 1 = MQTT
 * 2 = Serial
 */

const char* ssid     = "eir25287583";
const char* password = "CindyElsa2022!";

// MQTT Config 
const char* server = "192.168.0.150";
WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 2 seconds");
      // Wait 5 seconds before retrying
      delay(2000);
    }
  }
}


void MQTTOutput() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int val = analogRead(APin);
  snprintf (msg, MSG_BUFFER_SIZE, "%4d", val);
  Serial.print(val);
  Serial.print("    ");
  Serial.print("Publish message: ");
  Serial.println(msg);
  client.publish("outTopic", msg);
  delay(5);
}

void cleanSerialOutput() {
  Serial.println(analogRead(APin));
  delay(5);
}

void serialOutput() {
  Serial.print(analogRead(APin));
  Serial.println(",0,4500");
  delay(10);
}


void setup() {
  // Setup Analogue Pin & Serial Port
  pinMode(APin, INPUT);
  Serial.begin(9600);

  // We start by connecting to a WiFi network
  Serial.println();
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

  // MQTT Setup
  client.setServer(server, 1883);
  client.setCallback(callback);
}

void loop() {
   if(OutMode == 1) {
      MQTTOutput();
   }else if(OutMode == 2) {
      serialOutput();
   } else {
      Serial.println("Error Incorrect mode selected.");
   }
}
