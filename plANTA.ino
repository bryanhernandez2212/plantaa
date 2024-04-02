#include <LiquidCrystal_I2C.h>

const int pinLM35 = A0;
const int pinSensorHumedad = A1;
const int pinRelay = 2;
const int pinLuminosidad = A3;
int valor;
const long A = 1000;
const byte B = 15;
const byte Rc = 10;
const byte humedadPlanta1 = 40;
const byte humedadPlanta2 = 41;
const byte humedadPlanta3 = 42;
String dataSerial;
String plantaSeleccionada;

int valorLM35;
float temperatura;
int valorHumedad;
float humedad;
float valorLuminosidad;
float temperaturaActual;
float luminosidadActual;
float humedadActual;
bool temperaturaInicial = true;
bool luminosidadInicial = true;
bool humedadInicial = true;
bool inicio = true;

LiquidCrystal_I2C lcd(0x27, 16, 2);

boolean bombaEncendida = false;
boolean bombaApagada = true;

unsigned long previousMillis = 0;
const long interval = 10000; // intervalo de 10 segundos

void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
  pinMode(pinRelay, OUTPUT);
}

void EnviarDatos(float valor) {
  Serial.println(valor);
}
void EnviarDatosSensores(String valor) {
  Serial.println(valor);
}

void estado(String estadoBomba) {
  Serial.println(estadoBomba);
}

void mostrarDatosSerial(int comando) {
  switch (comando) {
    case 2:
      if (temperaturaInicial) {
        EnviarDatosSensores("tr:2:"+String(temperatura));
        temperaturaInicial = false;
      } else {
        valorLM35 = analogRead(pinLM35);
        temperaturaActual = (valorLM35 * 0.48828125);
        if (temperatura == temperaturaActual) {
          EnviarDatosSensores("tr:2");
        } else {
          EnviarDatosSensores("tr:2:"+String(temperaturaActual));
        }
      }
      break;

    case 3:
      if (luminosidadInicial) {
          EnviarDatosSensores("tr:3:"+String(valorLuminosidad));
        luminosidadInicial = false;
      } else {
        valor = analogRead(pinLuminosidad);
        luminosidadActual = ((long)valor * A * 10) / ((long)B * Rc * (1024 - valor));
        if (valorLuminosidad == luminosidadActual) {
          EnviarDatosSensores("tr:3");
        } else {
          EnviarDatosSensores("tr:3:"+String(luminosidadActual));
        }
      }
      break;

    case 4:
      if (humedadInicial) {
        EnviarDatosSensores("tr:4:"+String(humedad));
        humedadInicial = false;
      } else {
        valorHumedad = analogRead(pinSensorHumedad);
        humedadActual = 100 - map(valorHumedad, 0, 1023, 0, 100);
        if (humedad == humedadActual) {
          EnviarDatosSensores("tr:4");
        } else {
        EnviarDatosSensores("tr:4:"+String(humedadActual));
        }
      }
      break;

    case 5:
      estado(bombaEncendida ? "bom:1" : "bom:0");
      break;
  }
}

void revisarEstadoPlanta(float humedad, byte humedadPlanta){
    if (humedad <= humedadPlanta) {
    digitalWrite(pinRelay, LOW);
    bombaEncendida = true;
    bombaApagada = false;
  } else {
    digitalWrite(pinRelay, HIGH);
    bombaEncendida = false;
    bombaApagada = true;
  }
}

void loop() {
  unsigned long currentMillis = millis();
    valorLM35 = analogRead(pinLM35);
    temperaturaActual = (valorLM35 * 0.48828125);
    valor = analogRead(pinLuminosidad);
    luminosidadActual = ((long)valor * A * 10) / ((long)B * Rc * (1024 - valor));
    valorHumedad = analogRead(pinSensorHumedad);
    humedadActual = 100 - map(valorHumedad, 0, 1023, 0, 100);
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    valorLM35 = analogRead(pinLM35);
    temperatura = (valorLM35 * 0.48828125);

    valorHumedad = analogRead(pinSensorHumedad);
    humedad = 100 - map(valorHumedad, 0, 1023, 0, 100);

    valor = analogRead(pinLuminosidad);
    valorLuminosidad = ((long)valor * A * 10) / ((long)B * Rc * (1024 - valor));
    if(inicio){

      EnviarDatosSensores("2:"+ String(temperatura));
      EnviarDatosSensores("3:"+ String(valorLuminosidad));
      EnviarDatosSensores("4:"+ String(humedad));
      inicio = false;
    }
    else{
      if(temperatura != temperaturaActual){
      EnviarDatosSensores("2:"+ String(temperatura));
      }
      if(valorLuminosidad != luminosidadActual){
      EnviarDatosSensores("3:"+ String(valorLuminosidad));
      }
      if(humedad != humedadActual){
      EnviarDatosSensores("4:"+ String(humedad));
      }
    }


  }

  revisarEstadoPlanta(humedad, humedadPlanta1);


  lcd.setCursor(0, 0);
  lcd.print("Temperatura:");
  lcd.setCursor(12, 0);
  lcd.print(temperatura);

  lcd.setCursor(0, 1);
  lcd.print("Humedad:");
  lcd.setCursor(9, 1);
  lcd.print(humedad);
  lcd.print("%");

  lcd.setCursor(0, 2);
  lcd.print("Luminosidad:");
  lcd.setCursor(13, 2);
  lcd.print(luminosidadActual);

  if (Serial.available() > 0) {
    // leer datos enviados por serial
    dataSerial = Serial.readString();
    plantaSeleccionada = dataSerial.substring(0, 3);
    String opcion = dataSerial.substring(3);
    int comando = opcion.toInt();
    mostrarDatosSerial(comando);
  }
}
