import csv
from pprint import pprint

from devclass import NetworkDevice
from devclass import NetworkDeviceIOS
from devclass import NetworkDeviceXR

#======================================================================
def read_devices_info(devices_file):

    devices_list = []

    file = open(devices_file,'r')   # Open the CSV file
    csv_devices = csv.reader(file)  # Create the CSV reader for file

    # Iterate through all devices in our CSV file
    for device_info in csv_devices:

        # Create a device object with this data
        if device_info[1] == 'ios':
 
            device = NetworkDeviceIOS(device_info[0],device_info[2],
                                      device_info[3],device_info[4])

        elif device_info[1] == 'ios-xr':
 
            device = NetworkDeviceXR(device_info[0],device_info[2],
                                     device_info[3],device_info[4])

        else:
            device = NetworkDevice(device_info[0],device_info[2],
                                   device_info[3],device_info[4])

        devices_list.append(device) # Append this device object to list

    return devices_list


 
#====================================================================
def print_device_info(device):

    print '-------------------------------------------------------'
    print '    Device Name:      ',device.name
    print '    Device IP:        ',device.ip_address
    print '    Device username:  ',device.username,
    print '    Device password:  ',device.password
    print '-------------------------------------------------------'

#====================================================================
def write_devices_info(devices_file, devices_list):

    print '---- Printing CSV output ------------------------------'

    # Create the list of lists with devices and device info
    devices_out_list = []  # create list for CSV output

    for device in devices_list:
        dev_info = [device.name,device.ip_address,device.interfaces != ""]
        devices_out_list.append(dev_info)
 
    pprint(devices_out_list)

    # Use CSV library to output our list of lists to a CSV file
    with open(devices_file, 'w') as file:
        csv_out = csv.writer(file)
        csv_out.writerows(devices_out_list)