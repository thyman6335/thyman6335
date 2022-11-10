from util import read_devices_info
from util import print_device_info
from util import write_devices_info

#====================================================================
# Main program: connect to device, show interface, display

devices_list = read_devices_info('csv-devices')  # read CSV info for all devices

for device in devices_list:

    print '==== Device ============================================================='

    device.connect()          # connect to this specific device
    device.get_interfaces()   # get interface info for this specific device

    print_device_info(device)   # print device details for this device

write_devices_info('csv-devices-out', devices_list)   # write CSV entry for all devices