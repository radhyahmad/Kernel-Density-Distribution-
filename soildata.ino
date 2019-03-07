#include <PubSubClient.h>
#include <ESP8266WiFi.h>
#include <Wire.h>
#include<OneWire.h>
#include<DallasTemperature.h>

#define ONE_WIRE_BUS D3
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

const char* ssid = "";
const char* password = "";
const char* mqtt_server = "";

int adcSoil = 0;

WiFiClient espClient;
PubSubClient client(espClient);
long lastData = 0;

void setup_wifi() {

  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  //WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void reconnect() {

  while (!client.connected()) {

    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX); 

    if (client.connect(clientId.c_str())) { 

      Serial.println("connected");
      digitalWrite(LED_BUILTIN, LOW);
      //client.publish("outputsensor/soildata", "soil_sensor value");
      

    } else {
      
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      digitalWrite(LED_BUILTIN, HIGH);

      delay(5000);
      
    }
  }
}

void setup() {

  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  Wire.begin();
  sensors.begin();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {

  if (!client.connected()) {
    
    reconnect();
  }

  client.loop();

  
  float tS = sensors.getTempCByIndex(0);
  adcSoil = analogRead(A0);
  sensors.requestTemperatures();
  
  String soilTemp = String(tS);
  String soilMoisture = String(adcSoil);
  
  
  String payload = "{\"soilTemperature\":";
  payload += soilTemp;
  payload += ",\"soilMoisture\":";
  payload += soilMoisture;
  payload += "}";
  
  char dataSensorSoil[150];
  
  long now = millis();

  if (now - lastData > 5000) {

    lastData = now;
    payload.toCharArray(dataSensorSoil, 150);
    client.publish("outputsensor/soildata", dataSensorSoil);
    Serial.println(dataSensorSoil);

   
  }
}
