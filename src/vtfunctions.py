import requests
from isExecFileV2 import isExecFile
import time
key = ''
files_to_encrypt = []
file_to_scan = ""

def vtscan(x) : 
    global file_to_scan
    if(x[1]<(3.2e+7)) : #file size limit in virustotal

        url = 'https://www.virustotal.com/vtapi/v2/file/scan'
        params = {'apikey': key}
        files = {'file': (file_to_scan, open(file_to_scan, 'rb'))}
        response = requests.post(url, files=files, params=params)
        md5_resource = response.json()['md5']
        vtreport(md5_resource)

#   else: #in case of files larger than 32MB: CURRENTLY UNAVAILABLE
#        #restricted api: must contact 
#        url = 'https://www.virustotal.com/vtapi/v2/file/scan/upload_url'
#        params = {'apikey':key}
#        response = requests.get(url, params=params)
#        upload_url = response.json()['upload_url']
#        
#        
#        files = {'file': (file_to_scan, open(file_to_scan, 'rb'))}
#        response = requests.post(upload_url, files=files)
#        md5_resource = response.json()['md5']
#        vtreport(md5_resource)                 

        
#%%

def vtreport(resource):
    global files_to_encrypt, file_to_scan
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': key , 'resource': resource }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("200: \n")
        result_positives = response.json()['positives']
        if result_positives >= 5: #if the positives are less than 5 then it is condemended as safe
            files_to_encrypt.append(file_to_scan)
    else:
        print("204: req/min exceeded")

#%%

def vt(directory):
    global file_to_scan
    execFiles = isExecFile(directory)
    if execFiles:
        flag = 0
        for x in execFiles:
            file_to_scan = x[0]
            print("flag : " , flag)
            vtscan(x)
            flag+=1
            if flag ==2:
                time.sleep(60)
                flag = 0
        print(files_to_encrypt)

#%%
