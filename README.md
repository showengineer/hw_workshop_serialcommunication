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

What to adapt in the pipeline:
1. on the python side, you can adapt the retrieved values from the port using the custom_indices_mapping() function, keep in mind the mind the form that the get_data_list() function requires
2. on the python side, you can adapt the datapoint before sending it to the arduino using the custom_data_mapping() function
3. on the arduino side, you can create an actuation based on the received data in the actuateData() function
4. on the arduino side, create a function that captures inputs and create new keys for the python side
