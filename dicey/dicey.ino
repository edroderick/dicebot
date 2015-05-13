/*
 Serial1 : Dynamixel_Poart
 Serial2 : Serial_Poart(4pin_Molex)
 Serial3 : Serial_Poart(pin26:Tx3, pin27:Rx3)
 
 TxD3(Cm9_Pin26) <--(Connect)--> RxD(PC)
 RxD3(Cm9_Pin27) <--(Connect)--> TxD(PC)
 */

#define DXL_BUS_SERIAL1 1 //Dynamixel on Serial1(USART1) <-OpenCM9.04 
#define DXL_BUS_SERIAL2 3 //Dynamixel on Serial2(USART2) <-LN101,BT210 
#define DXL_BUS_SERIAL3 3 //Dynamixel on Serial3(USART3) <-OpenCM 485EXP

Dynamixel Dxl(DXL_BUS_SERIAL1);

char inChar;
byte index = 0;
int maxspeed = 400;
double inspeed;
int clawangle = 300;
int clawStep = 15;
int maxclaw = 1023;
int minclaw = 300;


void setup() {
  // Set up the pin 10 as an output:
  pinMode(BOARD_LED_PIN, OUTPUT);
  Serial3.begin(9600);
  Dxl.begin(3);
  Dxl.jointMode(1); //LeftClaw
  Dxl.jointMode(2); //RightClaw
  Dxl.wheelMode(3); //LeftWheel
  Dxl.wheelMode(4); //RightWheel
  Dxl.jointMode(5); //Catapult
  }


void loop() {

  delay(500);
  if(Serial3.available() > 0){
    char inData[20];
    while(Serial3.available()>0){
      if(index < 19){
        inChar = Serial3.read(); //read a character
        inData[index] = inChar;
        index++;
        inData[index] = '\0';
      }
    }
  
  index = 0;
  
  //inspeed = (double)inData[1]/255.0;
  
  SerialUSB.println(inData);
  
  //forward
  if(inData[0] == char(70)){
    Dxl.goalSpeed(4, maxspeed | 0x400);
    Dxl.goalSpeed(3, maxspeed); 
    delay(50);
  }
  //back
  if(inData[0] == char(66)){
    Dxl.goalSpeed(4, maxspeed);
    Dxl.goalSpeed(3, maxspeed | 0x400);
    delay(50);
  }
  //left
  if(inData[0] == char(76)){
    Dxl.goalSpeed(3, maxspeed/2 | 0x400);
    Dxl.goalSpeed(4, maxspeed/2 | 0x400);
    delay(50);
  }
  //right
  if(inData[0] == char(82)){
    Dxl.goalSpeed(3, maxspeed/2);
    Dxl.goalSpeed(4, maxspeed/2);
    delay(50);
  }
  //up
  //if(inData[0] == char(85)){
  //  Dxl.goalSpeed(3, maxspeed/4 | 0x400);
  //}
  //down
  //if(inData[0] == char(68)){aa
  //  Dxl.goalSpeed(3, maxspeed/4);
  //}
  //close claw
  if(inData[0] == char(79)){
    clawangle = clawangle + clawStep;
    Dxl.goalPosition(1, clawangle);
    Dxl.goalPosition(2, clawangle);
  }
  //open claw
  if(inData[0] == char(67)){
    clawangle = clawangle + clawStep;
    Dxl.goalPosition(1, clawangle | 0x400);
    Dxl.goalPosition(2, clawangle | 0x400);
  }
  
  //trigger catapult
  if(inData[0] == char(84)){
    Dxl.goalPosition(5, 900);
    delay(1000);
    Dxl.goalPosition(5, 490);    
  }
  //stop
  if(inData[0] == char(83)){
    Dxl.goalSpeed(1, 0);
    Dxl.goalSpeed(2, 0);
    Dxl.goalSpeed(3, 0);
    Dxl.goalSpeed(4, 0);
    Dxl.goalSpeed(5, 0);
  }
  delay(10);
}
}


