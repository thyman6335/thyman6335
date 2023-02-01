import csv
import requests

# Infoblox API endpoint
url = "https://infoblox.example.com/wapi/v2.10/record:host"

# Authentication credentials
auth = ("username", "password")

# Read the CSV file
with open("dns_entries.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row
    next(reader)
    for row in reader:
        hostname = row[0]
        # Search for the DNS entry
        search_url = url + "?name=" + hostname
        search_response = requests.get(search_url, auth=auth)
        search_data = search_response.json()
        if search_data:
            # Get the reference of the DNS entry
            ref = search_data[0]["_ref"]
            # Delete the DNS entry
            delete_url = url + "/" + ref
            requests.delete(delete_url, auth=auth)
            print(f"DNS entry for {hostname} deleted.")
        else:
            print(f"DNS entry for {hostname} not found.")