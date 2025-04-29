// Change this to the expected size, check the python terminal for the correct number.
const int expectedDataSize = 3;
const int motorPins[] = {3, 11, 1};
typedef struct {
  String column; 
  int row;
} DataSelection;

String data[expectedDataSize];

DataSelection encodeInputs(String colName, int rowNum){
  // do something with inputs to create a column key and row index
  Serial.println(colName);
  Serial.println(buildSerialString(colName, String(rowNum)));
  DataSelection selectionKeys {
    colName, rowNum
   };
  // return something in the shape of the given struct.
  return selectionKeys;
}

void requestData(DataSelection keys) {
   Serial.println(buildSerialString(keys.column, String(keys.row)));
}

String buildSerialString(String key, String index){
  String stringConcat = "{col:" + key + ",row:" + index + "}";
  return stringConcat;
}

String readSerialData(char endChar){
  String data = "";
  while(Serial.peek() != endChar){
   char ch = Serial.read();
   if(ch != '#') {
    data.concat(ch);
   }
  }
  char clean = Serial.read();
  
  return data;
}

void putReceivedDataStringInData(String dirtyString){
  String subString = dirtyString;
  int i = 0;
  while (dirtyString.indexOf("$") >= 0) {
    data[i++] = dirtyString.substring(0, dirtyString.indexOf("$"));
    dirtyString = dirtyString.substring(dirtyString.indexOf("$") + 1, dirtyString.length());
    Serial.println(dirtyString);
  }
  data[i] = dirtyString;
}

void actuateOnData(String data[expectedDataSize]){
  // actuate something based on the retrieved data
  for (int i = 0; i < expectedDataSize; i++) {  // three motors three country names
    int pwmValue =  data[i].toInt();    // read value
    pwmValue = constrain(pwmValue, 90, 255); //range (check for 90 cause thats when motor starts)
    analogWrite(motorPins[i], pwmValue);   // put into motor
  }

}

void setup() {
  pinMode(A5, INPUT);
  pinMode(3, OUTPUT);
  pinMode(11, OUTPUT);
  Serial.begin(9600);
  Serial.println("Connection established");
}

void loop() {  
  int potValue = analogRead(A5);
  int year = min(map(potValue, 0, 750, 1901, 2017), 2017);
  DataSelection keys = encodeInputs(String(year), -1);
  requestData(keys);
  
  delay(100);
  
  while(Serial.available() > 0){
    // if bytes available, retrieve data
    String receivedData = "";
    receivedData = readSerialData('#');
    putReceivedDataStringInData(receivedData);
    // actuate
    actuateOnData(data);
  }


}
