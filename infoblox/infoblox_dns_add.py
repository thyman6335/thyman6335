import csv
import requests

# Infoblox WAPI endpoint and credentials
wapi_url = "https://infoblox.example.com/wapi/v2.9/"
username = "admin"
password = "password"

# CSV file containing DNS entries to add
csv_file = "dns_entries.csv"

# Read DNS entries from CSV file
with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        ip_address = row["ip_address"]
        dns_name = row["dns_name"]

        # Check if DNS entry already exists
        url = f"{wapi_url}record:a?name={dns_name}"
        response = requests.get(url, auth=(username, password))
        if response.status_code == 200:
            data = response.json()
            for record in data:
                if record["ipv4addr"] == ip_address:
                    print(f"WARNING: DNS entry for {ip_address} already exists.")
                    continue

        # Add DNS entry
        url = wapi_url + "record:a"
        payload = {
            "name": dns_name,
            "ipv4addr": ip_address
        }
        response = requests.post(url, json=payload, auth=(username, password))
        if response.status_code == 201:
            print(f"Successfully added DNS entry for {ip_address}.")
        else:
            print("Error adding DNS entry.")
