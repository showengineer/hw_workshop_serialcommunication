typedef struct {
  String column; 
  int row;
} dataSelection;

dataSelection encodeInputs(String colName, int rowNum){
  // do something with inputs to create a column key and row index
  dataSelection selectionKeys {
    colName, rowNum
   };
  // return something in the shape of the given struct.
  return selectionKeys;
}

void requestData(dataSelection keys){
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

String cleanReceivedDataString(String dirtyString){
  String subString = dirtyString;
  int i = 0;
  String dataItems[];
  while(subString.indexOf("$") > 0){
    dataItems[i] = subString.substring(0, dirtyString.indexOf("$"));
    subString = subString.substring(dirtyString.indexOf("$"), dirtyString.length)); 
    i++;
  }
  return dataItems;
}

void actuateOnData(String data[]){
  if(data[0].equals("Aalsmeer")) {
    digitalWrite(12, LOW); 
  } else {
    digitalWrite(12, HIGH); 
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  dataSelection keys = encodeInputs("Municipalities", 1);
  requestData(keys);
  digitalWrite(12, HIGH); 
}

String data[];

void loop() {  
  while(Serial.available() > 0){
    // if packets available, retrieve data
    String receivedData = "";
    receivedData = readSerialData('#');
    data = cleanReceivedDataString(receivedData);
    // actuate something
    actuateOnData(data);
  }

  // process inputs and request new data
  int inputVal = analogRead(A0);
  delay(200);
  dataSelection keys = encodeInputs("Municipalities", map(inputVal, 0, 1023, 0, 341));
  requestData(keys);
}
