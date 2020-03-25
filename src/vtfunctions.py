import requests
from isbinaryfiles import isbinaryFiles

key = ''

def vtscan(directory) : 
    
    _, binaryFiles = isbinaryFiles(directory)
    #print(binaryFiles)
    for x in binaryFiles:
        if not x:
            continue
        file_to_scan = x[0]
        
        if(x[1]<(3.2e+7)) : #file size limit in virustotal
    
            url = 'https://www.virustotal.com/vtapi/v2/file/scan'
            params = {'apikey': key}
            files = {'file': (file_to_scan, open(file_to_scan, 'rb'))}
            response = requests.post(url, files=files, params=params)
            #print(response.json())

        else : #in case of files larger than 32MB
            #restricted api: must contact 
            url = 'https://www.virustotal.com/vtapi/v2/file/scan/upload_url'
            params = {'apikey':key}
            response = requests.get(url, params=params)
            upload_url = response.json()['upload_url']
            
            
            files = {'file': (file_to_scan, open(file_to_scan, 'rb'))}
            response = requests.post(upload_url, files=files)
            
        md5_resource = response.json()['md5']
        print(md5_resource)
        vtreport(md5_resource,file_to_scan)
        
#%%

def vtreport(resource,file_to_scan):

    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': key , 'resource': resource }
    response = requests.get(url, params=params)
    result_positives = response.json()['positives']
    if not result_positives:
        print("No malicious software detected")
    else:
        print("Malicious software detected: " + file_to_scan)

#%%
