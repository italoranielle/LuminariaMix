#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

WiFiUDP conexao;//Cria um objeto da classe UDP.
char pacote2[9];//String que armazena os dados recebidos pela rede.
int r,g,b,rp=2,gp=0,bp=4,lamp=1;

void setup() {
  pinMode(lamp,OUTPUT);
  pinMode(rp,OUTPUT);
  pinMode(gp,OUTPUT);
  pinMode(bp,OUTPUT);
  Serial.begin(9600);
  analogWrite(rp,1023);
  analogWrite(gp,1023);
  analogWrite(bp,1023);
  Serial.print("criando host");
  WiFi.mode(WIFI_AP);//Define o ESP8266 como Acess Point.
  WiFi.softAP("lamp", "");//Cria um WiFi de nome "NodeMCU" e sem senha.
  delay(2000);//Aguarda 2 segundos para completar a criaçao do wifi.
  conexao.begin(3333);
  Serial.print("criado");
  Serial.println(WiFi.localIP());

}

void loop() {
  int tamanhoPacote = conexao.parsePacket();
   if(tamanhoPacote == 9){
    conexao.read(pacote2,9);
    r = ((String(pacote2).substring(0,3)).toInt());
    g = ((String(pacote2).substring(3,6)).toInt());
    b = ((String(pacote2).substring(6,9)).toInt());
    r=1023-(map(r,0,255,0,1023));
    g=1023-(map(g,0,255,0,1023));
    b=1023-(map(b,0,255,0,1023));
    analogWrite(rp,r);
    analogWrite(gp,g);
    analogWrite(bp,b);
   
   }
}
