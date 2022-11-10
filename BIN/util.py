import json
from pprint import pprint

from devclass import NetworkDevice
from devclass import NetworkDeviceIOS
from devclass import NetworkDeviceXR

#======================================================================
def read_devices_info(devices_file):

    devices_list = []

    # Open the device file with JSON data and read into string
    json_file = open(devices_file,'r')   # open the JSON file
    json_device_data = json_file.read()  # read in the JSON data from file

    # Convert JSAON string into Python data structure
    devices_info_list = json.loads(json_device_data)

    for device_info in devices_info_list:

        # Create a device object with this data
        if device_info['os'] == 'ios':
 
            device = NetworkDeviceIOS(device_info['name'],device_info['ip'],
                                      device_info['user'],device_info['password'])

        elif device_info['os'] == 'ios-xr':
 
            device = NetworkDeviceXR(device_info['name'],device_info['ip'],
                                     device_info['user'],device_info['password'])

        else:
            device = NetworkDevice(device_info['name'],device_info['ip'],
                                   device_info['user'],device_info['password'])

        # Open SSH key file for this device
        key_file_path = "sshkeys/"+device_info['ip']+"/"+device_info['key']
        key_file = open(key_file_path,'rb')

        key_data = key_file.read()    # read ssh key data
        device.set_sshkey(key_data)   # store ssh key data in device object

        devices_list.append(device) # Append this device object to list

    return devices_list


 
#====================================================================
def print_device_info(device):

    print '-------------------------------------------------------'
    print '    Device Name:      ',device.name
    print '    Device IP:        ',device.ip_address
    print '    Device username:  ',device.username,
    print '    Device password:  ',device.password
    print '    Device key:       ',
    for c in device.sshkey: print c.encode('hex'),
    print '\n-------------------------------------------------------'

#====================================================================
def write_devices_info(devices_file, devices_list):

    print '---- Printing JSON output ------------------------------'

    # Create the list of lists with devices and device info
    devices_out_list = []  # create list for JSON output

    for device in devices_list:
        dev_info = {'name':device.name,'ip':device.ip_address,'os':device.os_type,
                    'user':device.username,'password':device.password}
        devices_out_list.append(dev_info)
 
    pprint(devices_out_list)

    # Convert the python device data into JSON for output to file
    json_device_data = json.dumps(devices_out_list)

    # Output the JSON string to a file
    with open(devices_file, 'w') as json_file:
        json_file.write(json_device_data)