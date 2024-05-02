import serial
import time
import pandas as pd

# save file in the same folder as the python file.
# file in the file name you need and add teh correct columns.
data = pd.read_excel('CATEGORIZABLE_municipalCapital.xlsx')
data_source = pd.DataFrame(data, columns=['Municipalities', 'Average capital (1 000 euro)'])

port = serial.Serial('COM3', 9600, timeout=.1)


def write_serial(value):
    value += '#'
    # print(value.encode('utf-8'))
    port.write(value.encode('utf-8'))
    time.sleep(0.05)


def read_serial(source):
    return source.read_until()


def get_indices_from_select_object(serial_string):
    # anticipated string: {col:col_name,row:row_number_int}
    # row_number  blank => entire column
    # column_name blank => entire row
    sliced_serial_list = serial_string[serial_string.find('{') + 1:serial_string.find('}')].split(',')
    indices_dict = {}

    for key_string in sliced_serial_list:
        key_value_list = key_string.split(':')
        indices_dict[key_value_list[0]] = key_value_list[1]

    return indices_dict


def get_data_list(source, keys):
    if keys['col'] == '':
        return source.iloc[int(keys['row'])].tolist()
    elif int(keys['row']) == -1:
        return source[keys['col']].tolist()
    return [source[keys['col']].values[int(keys['row'])]]


# return the list of data items as a string with $ between all items.
def get_serial_string_from_list(data_items_list):
    return '$'.join(map(str, data_list))


if __name__ == '__main__':
    while True:
        # wait for input from serial read
        while port.in_waiting:
            retrieved_data = read_serial(port)
            print("retrieve", retrieved_data)
            decoded_data = retrieved_data.decode('utf-8')
            print("decoded" + decoded_data)
            if decoded_data.startswith('{'):
                indices = get_indices_from_select_object(decoded_data)
                # do something with the indices
                data_list = get_data_list(data_source, indices)
                # do something with the elements in data_list
                print(get_serial_string_from_list(data_list))
                write_serial(get_serial_string_from_list(data_list))
