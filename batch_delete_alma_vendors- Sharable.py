import pandas as pd
import requests

#Set up default things for base URL and config API key
alma_base = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1'
acqapi = '[ENTER ACQ R/W KEY HERE]'
headers = {"Accept": "application/xml"}

#Take user input for input and output filenames 
fileToCheck = input("Enter file name of input Excel file (without '.xlsx' extension): ")
outputFileName = input("Enter name for output Excel file (without '.xlsx' extension): ")

#Import input file
df = pd.read_excel(f'{fileToCheck}.xlsx', dtype='str', keep_default_na=False)

vendor_code_raw = df['code'].astype(str)
vendor_name_raw = df['name'].astype(str)
print(vendor_code_raw[0])

#Set dict for reporting
dict= {}
dict['Vendor Code'] = []
dict['Vendor Name'] = []
dict['Delete Status'] = []
dict['Error Text'] = []

#Remove vendor by code and append details to dict for report
for i, vendor_code in enumerate(vendor_code_raw, 0):
    print(f"Checking record # {str(i+1)} of {str(len(vendor_code_raw))}")
    vendor_code = vendor_code_raw[i]
    vendor_name = vendor_name_raw[i]

    r_del = requests.delete(f"{alma_base}/acq/vendors/{vendor_code}?apikey={acqapi}", headers=headers)

    statuscode = r_del.status_code

    if statuscode == 400:
        errortext = r_del.text
    else:
        errortext = ""

    dict['Vendor Code'].append(vendor_code)
    dict['Vendor Name'].append(vendor_name)
    dict['Delete Status'].append(statuscode)
    dict['Error Text'].append(errortext)

#Convert dict to DF
df = pd.DataFrame(dict)

#Save DF as Excel file
df.to_excel(f"{outputFileName}.xlsx", index=False)