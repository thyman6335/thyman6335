import csv
from pprint import pprint

import sqlite3

from time import strftime
from time import localtime
from time import sleep
from time import time

from devclass import NetworkDevice
from devclass import NetworkDeviceIOS

#======================================================================
def read_devices_db(devices_db_file):

    print '---- reading devices from db ----------------------------'

    # Connect to the database and get a connection
    db_connection = sqlite3.connect(devices_db_file) # DB connection
    db_cursor = db_connection.cursor()               # DB cursor

    db_cursor.execute('SELECT * FROM devices')
    devices_from_db = db_cursor.fetchall()

    pprint(devices_from_db)
    print '---- end devices from db --------------------------------'

    # Done adding devices to the table, close it down.
    db_cursor.close()
    db_connection.close()
 
    return devices_from_db

#======================================================================
def get_device(devices_from_db, device_ip):

    for device_info in devices_from_db:

        # Create a device object with this data
        if device_info[1] == device_ip and device_info[2] == 'ios':
 
            return  NetworkDeviceIOS(device_info[0],device_info[1],
                                      device_info[3],device_info[4])

    return None

 
#=======================================================================
def gather_traffic_data(logfile, device, interface, interval, count):

    # Reset the log file to begin fresh
    dev_stats_log = open(logfile,'w') 
    dev_stats_log.close()

    # Loop for 'num_readings' number of times
    for _ in range(count):  # Loop the specified number of times

        print ''
        print '---- reading rx, tx data ------------------------------'

        dev_stats_log = open(logfile,'a') # open the file for appending

        # Get the rx and tx stats for a specific interface on device
        device.connect()
        stats = device.get_interface_stats(interface)   

        print '    ---- ',device.ip_address,' : stats: ',stats

        # Write rx and tx information to database 
        write_stats_log(dev_stats_log, time(), device.ip_address,
                            stats[0], stats[1], stats[2], stats[3])

        dev_stats_log.close()  # Done appending to file for now

        print ''
        sleep(interval)  # Pause the defined interval


#======================================================================
def write_stats_log(file, time, ip_address,
                                rx_packets, rx_bytes,
                                tx_packets, tx_bytes):

     # Create a log entry from the data given
     log_entry = [time, ip_address, rx_packets, rx_bytes,
                                    tx_packets, tx_bytes]

     log = csv.writer(file)
     log.writerow(log_entry)


 
#======================================================================
def print_log(device_ip_address, log_info_list):

    print '  Time        Rx Packets    Rx Bytes  Tx Packets    Tx Bytes     Util'
    print '  ----------  ----------  ----------  ----------  ----------  -------'

    last_bytes = 0

    for log_entry in log_info_list:

        if log_entry[1] != device_ip_address: # Ignore if not passed IP address
            continue

        if last_bytes == 0:    # if first calculation, set util to 0
            util = 0
            last_bytes = int(log_entry[3]) + int(log_entry[5])
            last_secs = float(log_entry[0])

        else:                        # else calculate lan utilization
            current_bytes = int(log_entry[3]) + int(log_entry[5])
            interval_bytes = current_bytes - last_bytes
       
            if_speed = 1000000000
            current_secs = float(log_entry[0])
            interval_time = current_secs - last_secs

            util = (interval_bytes*8*100) / float(interval_time*if_speed)

            last_bytes = current_bytes
            last_secs  = current_secs

        str_time = strftime('%H:%M:%S', localtime(float(log_entry[0])))
        print '  {0:10}  {1:>10}  {2:>10}  {3:>10}  {4:>10}  {5:>7.3f}'.format(str_time,
                                                      log_entry[2], log_entry[3],
                                                      log_entry[4], log_entry[5],
                                                      util)
 