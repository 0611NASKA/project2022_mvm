unsigned long prev, next, interval;
int times = 0;
int status =0;
int times1 = 0;
int button = 3;  
void setup() {
  Serial.begin(9600);
  prev = 0; 
  interval = 2000;
  pinMode(0, INPUT);//0番ピンを入力に設定

  
 
}
 
void loop() {
    if(digitalRead(0) == 0) {//0番ピンのスイッチがONの場合、実行
    Serial.println(button);//「count」を送信、改行
    while(digitalRead(0) == 0) {//0番ピンのスイッチがONの場合、繰り返す
      delay(10);//10msec待機(0.01秒待機)、チャタリング対策
    }
  }
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


unsigned long curr = millis();    // 現在時刻を取得
  if ((curr - prev) >= interval) {  // 前回実行時刻から実行周期以上経過していたら
    // do periodic tasks            // 周期処理を実行
//    if(head < 1000)
//       times = times + 1;
//    if(times >= 3)
//       status = 1;
    times = 0;
    times1 = 0;
    status = 0;
       
    //Serial.println(times);
    prev = curr;                    // 前回実行時刻を現在時刻で更新
  }else{
    
    if(head < 1000)
       times = times + 1;
    if(times >= 5)
       status = 1;
    if((y > 1000)||(y < -1000))
       times1 = times1 + 1;
    if(times1 >= 2)
       status = 2;
    }

    



//-----出力-----
////上下
//    Serial.print("Z : ");
      //Serial.println(z);
////前後
//    Serial.print("Y : ");
   // Serial.println(y);
////左右
//    Serial.print("X : ");
//    Serial.println(x);
////感圧センサー
//    Serial.print("head:");
      //Serial.println(head);    
      //Serial.print("status:");
     // Serial.println(times1);
       //Serial.write('H');             // ヘッダの送信
      //Serial.write(highByte(status)); // 上位バイトの送信
      //Serial.write(lowByte(status));  // 下位バイトの送信
      Serial.println(status);
      delay(100);
}