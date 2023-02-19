#include <Wire.h>
#include <LiquidCrystal_I2C.h>

int E1 = 3;
int M1 = 12;
int E2 = 11;
int M2 = 13;


String inputString;
LiquidCrystal_I2C lcd(0x3F, 20, 4);


int val;
int PWM;
int LED = 13;
void setup()
{
  lcd.init();                            // Инициализация lcd
  lcd.backlight();                       // Включаем подсветку
  // Курсор находится в начале 1 строки
  lcd.print("Hello, world!");            // Выводим текст
  lcd.setCursor(0, 1);


  Serial.begin(9600);
  //  pinMode(LED, OUTPUT);
  //  digitalWrite(LED, HIGH);
  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);

  Serial.println("Запуск...");
}

byte buffer[255];
void loop()
{
  //Serial.println("Цикл");
  if (Serial.available())
  {
    Serial.readBytesUntil(10, buffer, 255);
    inputString = buffer;
    //    go(val);
    Serial.println(inputString);
    Serial.println((int) inputString[0]);
    lcd.clear();
    lcd.print(inputString);
  }
}

void go(int val) {
  val = Serial.read();
  if (val == 'w')
  {
    //      Serial.println("Едем в перёд");
    digitalWrite(M1, HIGH);
    digitalWrite(M2, HIGH);
    analogWrite(E1, 200); // PWM regulate speed
    analogWrite(E2, 200); // PWM regulate speed
  }
  if (val == 's')
  {
    //      Serial.println("Едем в назад");
    digitalWrite(M1, LOW);
    digitalWrite(M2, LOW);
    analogWrite(E1, 200); // PWM regulate speed
    analogWrite(E2, 200); // PWM regulate speed
  }
  if (val == 'd')
  {
    //      Serial.println("Поворачиваем на лево");
    digitalWrite(M1, LOW);
    digitalWrite(M2, HIGH);
    analogWrite(E1, 200); // PWM regulate speed
    analogWrite(E2, 200); // PWM regulate speed
  }
  if (val == 'a')
  {
    //      Serial.println("Поворачиваем на право");
    digitalWrite(M1, HIGH);
    digitalWrite(M2, LOW);
    analogWrite(E1, 200); // PWM regulate speed
    analogWrite(E2, 200); // PWM regulate speed
  }
  if (val == 'p')
  {
    //      Serial.println("Стоп");
    analogWrite(E1, 0); // PWM regulate speed
    analogWrite(E2, 0); // PWM regulate speed
  }
  //    else {
  //      analogWrite(E1, 210); // PWM regulate speed
  //      analogWrite(E2, 210); // PWM regulate speed
  //    }
}
