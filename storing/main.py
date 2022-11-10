from util import read_devices_db
from util import get_device
from util import gather_traffic_data
from util import write_stats_log
from util import print_log

from sys import argv
import csv

#====================================================================
# Main program: read devices, then get traffic statistics from each

# Get arguments passed to our application
print 'argv: ',argv
interval  = int(argv[1]) if len(argv) >= 2 else 5
count     = int(argv[2]) if len(argv) >= 3 else 5
device_ip = argv[3]      if len(argv) >= 4 else '10.30.30.1'
interface = argv[4]      if len(argv) >= 5 else 'gigabitethernet 0/1'

# Read device information from database, into list of device info lists
devices_from_db = read_devices_db('devices.db')

# Get device information for our device
device = get_device(devices_from_db, device_ip)
if device == None:
    print '!!! Cannot find device in DB!'
    exit()

logfile = 'dev-stats-log'  # set output CSV log file

# Gather traffic data for the devices in the list
gather_traffic_data(logfile, device, interface, interval, count)

dev_stats_log = open(logfile,'r')
csv_log = csv.reader(dev_stats_log)

log_info_list = [log_info for log_info in csv_log]

# Print log information for our one device
print ''
print 'Device: ', device.ip_address, '  Interface: ', interface
print ''

print_log(device_ip, log_info_list)