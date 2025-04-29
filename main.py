import serial
import time
import pandas as pd

# save file in the same folder as the python file.
# file in the file name you need and add the correct columns.
file_name = 'CONTINUOUS_TIME_GreenhouseGasses.xlsx'
columns_name_list = [x for x in range(1901, 2018)]
connected_port = 'COM4'

# DO NOT TOUCH
data = pd.read_excel(file_name)
data_source = pd.DataFrame(data, columns=columns_name_list)
comm_port = serial.Serial(connected_port, 9600, timeout=.1)


def write_serial(value, dest):
    value += '#'
    dest.write(value.encode('utf-8'))
    time.sleep(0.05)


def read_serial(source):
    # by default, it reads until a '\n' character
    return source.read_until()


# requires a keys dictionary in the form:
# keys = {
# 'col': 'col_name',
# 'row': 'row_number'
# }
def get_indices_from_select_object(serial_string):
    # row_number  -1 => return entire column
    # column_name '' => return entire row
    sliced_serial_list = serial_string[serial_string.find('{') + 1:serial_string.find('}')].split(',')
    indices_dict = {}

    for key_string in sliced_serial_list:
        key_value_list = key_string.split(':')
        indices_dict[key_value_list[0]] = key_value_list[1]

    return indices_dict


# requires a dictionary in the form:

def get_data_list(source, keys):
    print(keys)
    if keys['col'] == '':
        return source.iloc[int(keys['row'])].tolist()
    elif int(keys['row']) == -1:
        return source[keys['col']].tolist()
    return [source[keys['col']].values[int(keys['row'])]]


# return the list of data items as a string with $ between all items.
def get_serial_string_from_list(data_items_list):
    return '$'.join(map(str, data_list))


def custom_indices_mapping(indices_dict):
    indices_copy = indices_dict
    # manipulate indices_copy if required
    return indices_copy


def custom_data_mapping(original_data_list):
    converted_data = original_data_list
    # manipulate converted_data if required
    return converted_data


if __name__ == '__main__':
    print('Starting python script')
    while True:
        # wait for input from serial read
        while comm_port.in_waiting:
            print('Reading serial data on port: ', connected_port)
            retrieved_data = read_serial(comm_port)
            decoded_data = retrieved_data.decode('utf-8')
            print('Received message: ', retrieved_data)
            if decoded_data.startswith('{'):
                indices = get_indices_from_select_object(decoded_data)
                # do something with the indices
                indices = custom_indices_mapping(indices)
                data_list = get_data_list(data_source, indices)
                print('Writing to: ', connected_port, ', data length: ', len(data_list))
                # do something with the elements in data_list
                data_list = custom_data_mapping(data_list)
                write_serial(get_serial_string_from_list(data_list), comm_port)
