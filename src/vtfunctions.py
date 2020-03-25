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
            #todo: fix JSONDecodeError: Expecting value
            url = 'https://www.virustotal.com/vtapi/v2/file/scan/upload_url'
            params = {'apikey':key}
            response = requests.get(url, params=params)
            #print(response.json())
            upload_url_json = response.json()
            upload_url = upload_url_json['upload_url']
            
            
            files = {'file': (file_to_scan, open(file_to_scan, 'rb'))}
            response = requests.post(upload_url, files=files)
            #print(response.json())
            
        md5_resource_json = response.json()
        md5_resource = md5_resource_json['md5']
        print(md5_resource)
        vtreport(md5_resource)
        
#%%

def vtreport(resource):

    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': key , 'resource': resource }
    response = requests.get(url, params=params)
    print(response.json())
    #todo: yet to extract info from response

#%%
