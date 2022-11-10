from util import read_devices_info
from util import print_device_info
from util import write_devices_info

#====================================================================
# Main program: connect to device, show interface, display

devices_list = read_devices_info('json-devices')  # read JSON info for all devices

for device in devices_list:

    print '==== Device ============================================================='

    device.connect()          # connect to this specific device
    device.get_interfaces()   # get interface info for this specific device

    print_device_info(device)   # print device details for this device

write_devices_info('json-devices-out', devices_list)   # write JSON entry for all devices

# Do it again, reading from our output file, to prove we did it correctly

print '-----------------------------------------------------------------------------'
print '---------- Reading from our output file, doing it again ---------------------'

devices_list = read_devices_info('json-devices-out')  # read JSON info for all devices

for device in devices_list:

    print '==== Device ============================================================='

    device.connect()          # connect to this specific device
    device.get_interfaces()   # get interface info for this specific device

    print_device_info(device)   # print device details for this device