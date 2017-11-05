import csv
from io import StringIO
from  more_itertools import unique_everseen
import requests

filename = r"C:\Users\Zander\Documents\python for social science\Wealth-Map\Code Complaint List20171024.csv"
url = 'https://geocoding.geo.census.gov/geocoder/locations/addressbatch'

fieldnames = ['Complaint Number',
              'address',
              'city',
              'state',
              'zip']

# Open the complaint file and read into a list of dicts
with open(filename, encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile)
    bam=list(reader)

# drop duplicates, of which there are several    
bam = list(unique_everseen(bam))

# format the addresses
for row in bam:
    row['address'] = row['Address'].split(',')[0]
    row['city'] = 'Atlanta'
    row['state'] = 'GA'
    row['zip'] = None

# drop the complaints with weird addresses, which is a small portion
dingo = [ bam[i] for i in range(0,len(bam)) if bam[i]['Address'].count(',') == 1 ]

#define parameters for 
data =  {'returntype': 'geographies',
            'benchmark': 'Public_AR_Current',
            'vintage': 'Current_Current'}

chunk = 1000
dinger = [ dingo[x:x+1000] for x in range(0, len(dingo), 1000) ]

for blorp in dinger:
    
    # write 1000 rows to a file
    with open('slammer.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n', extrasaction='ignore')
        writer.writerows(blorp)
    
    # geocode those 1000 rows
    files = { 'addressFile':  open('slammer.csv', 'r') }
    r = requests.post(url, files=files, data=data)
    
    # append results to our results file
    with open('geocoded.csv', 'a') as resultfile:
        resultfile.write(r.text)
    
    print("geocoded a batch")
