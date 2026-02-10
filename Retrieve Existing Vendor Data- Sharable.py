import pandas as pd
import requests
from bs4 import BeautifulSoup

#Set up default things for base URL and config API key
alma_base = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1'
acqapi = '[ENTER ACQ R/W OR R/O KEY HERE]'
headers = {"Accept": "application/xml"}

#Take user input for input and output filenames 
fileToCheck = input("Enter file name of input Excel file (without '.xlsx' extension): ")
outputFileName = input("Enter name for output Excel file (without '.xlsx' extension): ")

#Import input file
df = pd.read_excel(f'{fileToCheck}.xlsx', dtype='str', keep_default_na=False)

vendor_code_raw = df['Vendor Code'].astype(str)
vendor_name_raw = df['Name'].astype(str)

#Set dict for retrieved data
dict= {}
dict['Vendor Code'] = []
dict['Vendor Name'] = []
dict['Existing PO lines'] = []
dict['Sample PO line'] = []

#Retreive vendor data and add to dict
for i, vendor_code in enumerate(vendor_code_raw, 0):
    print(f"Checking record # {str(i+1)} of {str(len(vendor_code_raw)+1)}")
    vendor_code = vendor_code_raw[i]
    vendor_name = vendor_name_raw[i]

    r = requests.get(f"{alma_base}/acq/po-lines?q=vendor_code~{vendor_code}&status=ALL_WITH_CLOSED&limit=10&offset=0&order_by=title&direction=desc&acquisition_method=ALL&apikey={acqapi}", headers=headers)

    if r.status_code == 200: 
        # Creating the Soup Object containing all data
        soup = BeautifulSoup(r.content, "xml")

        try:
            linescount = int(soup.po_lines['total_record_count'])
        except AttributeError:
            linescount = 0

        try:
            samplePO = soup.find('po_number').getText()
        except AttributeError:
            samplePO = ""
    
    else:
        linescount = "retrieval error"
        samplePO = "retrieval error"
    
    dict['Vendor Code'].append(vendor_code)
    dict['Vendor Name'].append(vendor_name)
    dict['Existing PO lines'].append(linescount)
    dict['Sample PO line'].append(samplePO)

#Convert dict to DF
df = pd.DataFrame(dict)

#Save DF as Excel file with previously-given filename
df.to_excel(f"{outputFileName}.xlsx", index=False)

