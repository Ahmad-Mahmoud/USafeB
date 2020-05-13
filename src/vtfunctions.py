import requests
from isExecFile import isExecFile

key = ''
reports = []
files_to_encrypt = []

def vtscan(directory) : 
    
    execFiles = isExecFile(directory)
    if execFiles:
        for x in execFiles:
           file_to_scan = x[0]
            
            if(x[1]<(3.2e+7)) : #file size limit in virustotal
        
                url = 'https://www.virustotal.com/vtapi/v2/file/scan'
                params = {'apikey': key}
                f iles = {'file': (file_to_scan, open(file_to_scan, 'rb'))}
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
            vtreport(md5_resource,file_to_scan)
    return files_to_encrypt

#%%

def vtreport(resource,file_to_scan):

    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': key , 'resource': resource }
    response = requests.get(url, params=params)
    result_positives = response.json()['positives']
    if result_positives >= 5: #if the positives are greater than or equal 5 then it is condemended as unsafe
        files_to_encrypt.append(file_to_scan)

#%%
