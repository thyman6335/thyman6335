import csv
import subprocess

# Open CSV file and read IP addresses
with open('ips.csv') as csvfile, open('results.csv', 'w', newline='') as resultfile:
    reader = csv.reader(csvfile)
    writer = csv.writer(resultfile)
    for row in reader:
        ip = row[0]

        # Ping IP address
        result = subprocess.call(['ping', '-c', '1', ip])

        # Check if online or offline
        if result == 0:
            status = 'online'
        else:
            status = 'offline'

        # Write result to new CSV file
        writer.writerow([ip, status])
