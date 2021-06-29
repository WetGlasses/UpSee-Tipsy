
/*
  servo1.attach(11);               
  servo2.attach(10);  
  servo3.attach(9);               
  servo4.attach(6);
  servo5.attach(5);               
  servo6.attach(3);

  :120,80,150,30,10;
  :50,30,70,00,80;
  
 */

#include <Servo.h>

Servo one;
Servo two;
Servo thr;
Servo fou;
Servo fiv;
Servo six;

float kp = 0.05;

int one_dest = 0; 
int two_dest = 135;
int thr_dest = 42;
int fou_dest = 87;  
int fiv_dest = 90;
int six_dest = 90;


float one_now = one_dest; 
float two_now = two_dest;
float thr_now = thr_dest;
float fou_now = fou_dest;  
float fiv_now = fiv_dest; 
float six_now = six_dest; 


void servo_setup()
{
  
  one.write(one_now); 
  two.write(two_now); 
  thr.write(thr_now); 
  fou.write(fou_now);
  fiv.write(fiv_now);
  six.write(six_now);

  one.attach(11);
  two.attach(10);
  thr.attach(9);
  fou.attach(6); 
  fiv.attach(5);
  six.attach(8);

}


void serial_setup()
{
  Serial.begin(9600);
  Serial.setTimeout(10);
  //Serial.println( String(one_now) + ' ' + String(two_now) + ' ' + String(thr_now) + ' ' + String(fou_now)  + ' ' + String(fiv_now) );
}

void update_now()
{

  one.write(one_now); 
  two.write(two_now); 
  thr.write(thr_now); 
  fou.write(fou_now);
  fiv.write(fiv_now);
  six.write(six_now);

  
}


void check_angle()
{
  if(not ((int(one_now) == one_dest) and (int(two_now) == two_dest) and (int(thr_now) == thr_dest) and (int(fou_now) == fou_dest)  and (int(fiv_now) == fiv_dest)and (int(six_now) == six_dest)))
  {

    one_now = one_now + kp* (one_dest - one_now);
    two_now = two_now + kp* (two_dest - two_now);
    thr_now = thr_now + kp* (thr_dest - thr_now);
    fou_now = fou_now + kp* (fou_dest - fou_now);
    fiv_now = fiv_now + kp* (fiv_dest - fiv_now);
    six_now = six_now + kp* (six_dest - six_now);

    update_now();
    delay(20);
    
  }
}


void decode_angle(String data)
{

  Serial.print(data);
  
  int angles[6];
  
  char *pch;
  
  char info[40];
  data.toCharArray(info, 40);

  pch = strtok (info,",");

  char angle_found = 0;
  
  while( pch != NULL )
  {
    angles[angle_found]= atoi(pch);
    angle_found = angle_found + 1 ; 
    pch = strtok (NULL ,",");  
  }

  one_dest = angles[0];
  two_dest = angles[1];
  thr_dest = angles[2];
  fou_dest = angles[3];
  fiv_dest = angles[4];
  six_dest = angles[5];

  //Serial.println( "Target: " +  String(one_dest) + ' ' + String(two_dest) + ' ' + String(thr_dest) + ' ' + String(fou_dest) + ' ' + String(fiv_dest));
  
}






void setup() 
{

  servo_setup();
  serial_setup();

}



void loop() 
{  

  if(Serial.available())
  {
    String data = Serial.readString();
    if((data[0] == ':') and (data[data.length()-1] == ';'))
    {
      Serial.println("New Angle Found");
      decode_angle(data.substring(1, data.length()-2));
    }
  }
  
  check_angle();
}
