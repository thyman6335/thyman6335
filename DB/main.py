from util import read_devices_info
from util import print_device_info
from util import write_devices_db
from util import read_devices_db

from pprint import pprint

#====================================================================
# Main program: connect to device, show interface, display

devices_list = read_devices_info('json-devices')  # read JSON info for all devices

for device in devices_list:

    print '==== Device ============================================================='

    device.connect()          # connect to this specific device
    device.get_interfaces()   # get interface info for this specific device

    print_device_info(device)   # print device details for this device

devices_db_file = 'devices.db'
write_devices_db(devices_db_file, devices_list)   # write device data to database

# Now read in the device information we just wrote
devices_from_db = read_devices_db(devices_db_file)

print '==== Device info from database ============================================='
pprint(devices_from_db)