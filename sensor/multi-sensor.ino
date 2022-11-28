void setup() {
  Serial.begin(9600);
}
 
void loop() {
  // 地球の重力である1Gの加速度(m/s^2)
  float ms2 = 9.80665;
  
  // 電源電圧5V時のオフセット電圧(0G = 2.5V = 2500mV)
  float offset_voltage = 2500.0;
 
  // XYZの電圧(mV)を取得する
  int x =  (analogRead(A0) / 1024.0) * 5.0 * 1000;
  int y =  (analogRead(A1) / 1024.0) * 5.0 * 1000;
  int z =  (analogRead(A2) / 1024.0) * 5.0 * 1000;
 
  // XYZからオフセット電圧を引いた電圧を求める
  x = x - offset_voltage;
  y = y - offset_voltage;
  z = z - offset_voltage;
  
//------感圧センサー------
   //赤、黒頭→センサー
  int head = analogRead(A3);
  //青、白→腹センサー
  int belly = analogRead(A4);
  // XYZから重力を求める
//  float xg = x / 1000.0;
//  float yg = y / 1000.0;
//  float zg = z / 1000.0;

//-----出力-----
//上下
    Serial.print("Z : ");
    Serial.println(z);
//前後
    Serial.print("Y : ");
    Serial.println(y);
//左右
    Serial.print("X : ");
    Serial.println(x);
//感圧センサー
    Serial.print("head:");
    Serial.println(head);
    Serial.print("belly:");
    Serial.println(belly); 
    
 
  delay(700);
}