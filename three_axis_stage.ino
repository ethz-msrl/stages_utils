/*
this file contains code for controlling the three axis stepper stage using an ATMEGA256P and DM542T stepper motor drivers
*/

#define ENA_PIN1 48
#define DIR_PIN1 49
#define PUL_PIN1 50

#define ENA_PIN2 44
#define DIR_PIN2 45
#define PUL_PIN2 46

#define ENA_PIN3 40
#define DIR_PIN3 41
#define PUL_PIN3 42

#define ENA_PIN4 36
#define DIR_PIN4 37
#define PUL_PIN4 38

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN,OUTPUT);
  pinMode(ENA_PIN1, OUTPUT);
  pinMode(DIR_PIN1,OUTPUT);
  pinMode(PUL_PIN1,OUTPUT);
  pinMode(ENA_PIN2, OUTPUT);
  pinMode(DIR_PIN2,OUTPUT);
  pinMode(PUL_PIN2,OUTPUT);
  pinMode(ENA_PIN3, OUTPUT);
  pinMode(DIR_PIN3,OUTPUT);
  pinMode(PUL_PIN3,OUTPUT);
  pinMode(ENA_PIN4, OUTPUT);
  pinMode(DIR_PIN4,OUTPUT);
  pinMode(PUL_PIN4,OUTPUT);
  pinMode(LED_BUILTIN,OUTPUT);

  Serial.begin(9600);
  delay(500);
}

char command_buffer[20];
char out_buffer[30];
unsigned int delay_us=250;
//commands for moving at regular speed
const char MOVEX_CMD[]="MOVEX";
const char MOVEY_CMD[]="MOVEY";
const char MOVEZ_CMD[]="MOVEZ";
const char SETSP_CMD[]="SETSP";

// the loop function runs over and over again forever
void loop() {
  delay(1000);
  digitalWrite(DIR_PIN1,HIGH);
  digitalWrite(ENA_PIN1,LOW);
  digitalWrite(DIR_PIN2,HIGH);
  digitalWrite(ENA_PIN2,LOW);
  digitalWrite(DIR_PIN3,HIGH);
  digitalWrite(ENA_PIN3,LOW);
  digitalWrite(DIR_PIN4,HIGH);
  digitalWrite(ENA_PIN4,LOW);
  delay(1000);
  unsigned int i=0;
  while(true){

    // Serial.write("XXXXXXXX");
    // delay(1000);
    // continue;


    //read the serial command
    Serial.setTimeout(100000);
    size_t count=Serial.readBytesUntil('\n',command_buffer,20);

    sprintf(out_buffer,"Command %s",command_buffer);
    Serial.write(out_buffer);

    command_buffer[count]='\0';

    //determine the command integer
    int32_t command_integer=atol(command_buffer+5);

    //determine the command
    command_buffer[5]='\0';

    if(strcmp(command_buffer,MOVEX_CMD)==0){
      sprintf(out_buffer,"Taking %ld steps in x...\n",command_integer);
      Serial.write(out_buffer);
      if(command_integer<0){
        digitalWrite(DIR_PIN1,HIGH);
        digitalWrite(DIR_PIN2,HIGH);
      }
      else{
        digitalWrite(DIR_PIN1,LOW);
        digitalWrite(DIR_PIN2,LOW);
      }
      command_integer=abs(command_integer);
      delay(10);
      //take steps in x direction
      for(i=0; i<command_integer; i++){
        digitalWrite(PUL_PIN1,LOW);
        digitalWrite(PUL_PIN2,LOW);
        delayMicroseconds(delay_us);
        digitalWrite(PUL_PIN1,HIGH);
        digitalWrite(PUL_PIN2,HIGH);
        delayMicroseconds(delay_us);
      }
      delayMicroseconds(100);
      Serial.println("COMPLETE\n");
    }
    if(strcmp(command_buffer,MOVEY_CMD)==0){
      sprintf(out_buffer,"Taking %ld steps in x...\n",command_integer);
      Serial.write(out_buffer);
      if(command_integer<0){
        digitalWrite(DIR_PIN3,LOW);
      }
      else{
        digitalWrite(DIR_PIN3,HIGH);
      }
      command_integer=abs(command_integer);
      delay(10);
      //take steps in x direction
      for(i=0; i<command_integer; i++){
        digitalWrite(PUL_PIN3,LOW);
        delayMicroseconds(delay_us);
        digitalWrite(PUL_PIN3,HIGH);
        delayMicroseconds(delay_us);
      }
      Serial.println("COMPLETE\n");
    }
    if(strcmp(command_buffer,MOVEZ_CMD)==0){
      sprintf(out_buffer,"Taking %ld steps in z...\n",command_integer);
      Serial.write(out_buffer);
      if(command_integer<0){
        digitalWrite(DIR_PIN4,LOW);
      }
      else{
        digitalWrite(DIR_PIN4,HIGH);
      }
      command_integer=abs(command_integer);
      delay(10);
      //take steps in x direction
      for(i=0; i<command_integer; i++){
        digitalWrite(PUL_PIN4,LOW);
        delayMicroseconds(delay_us);
        digitalWrite(PUL_PIN4,HIGH);
        delayMicroseconds(delay_us);
      }
      Serial.println("COMPLETE\n");
    }
    if(strcmp(command_buffer,SETSP_CMD)==0){
      delay_us=command_integer;
      if(delay_us<10)
        delay_us=10;
      Serial.println("COMPLETE\n");
    }

  }
}
