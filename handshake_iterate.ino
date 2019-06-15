
int V= 0;

// the setup routine runs once when you press reset:
void setup() {
        // on démarre la liaison
        // en la réglant à une vitesse de 115200 bits par seconde.
        Serial.begin(115200);
}
void loop() {
  // main code here, that runs repeatedly:

  // Setup pins for input
  //handshake test only execute when receive command
    if(Serial.read()=='K')
        {
          for (int i = 0; i < 6; i++) { 
                      int V = analogRead(i);
                      Serial.print(V);
                      Serial.print(" ");
                      Serial.print(i);
                  }
        }
}
