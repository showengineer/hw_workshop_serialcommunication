How to collect the correct data:
1. clone this repository
2. add the name of the file you want to use in the file_name variable in the main.py file
3. add the columns of this file in the columns_name_list variable in the main.py file
4. add the port to which the arduino is connected in the connected_port variablein the main.py file
5. add the size of the expected data in the arduino_serial_communication.ino file

How to use the communication:
1. upload arduino_serial_communication.ino to an arduino
2. press and hold the reset button on the arduino
3. run the main.py file on the connected laptop
4. when the python run terminal shows 'Starting python script', release the reset button
5. the python ron terminal should start reading data and printing the string that is received
