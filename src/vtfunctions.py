
import requests
from isExecFileV2 import isExecFile
import time
key = ''
files_to_encrypt = []
file_to_scan = ""
#This segment of code uses VirusTotal API for scanning suspected files
#Check VirusTotal API documentation V2 for reference

#This method takes a filename, uploads the file to be scanned,
#and uses the output md5 to access the report on the file
def vtscan(x) : 
    global file_to_scan
    if(x[1]<(3.2e+7)) : #file size limit in free VirusTotal service

        url = 'https://www.virustotal.com/vtapi/v2/file/scan'
        params = {'apikey': '42c175b53b9749272ebe4a5019679045b8a590aeb8f1dc87c91e6ad807121d72'}
        files = {'file': (file_to_scan, open(file_to_scan, 'rb'))}
		#posts request to API using URL and key given account
        response = requests.post(url, files=files, params=params)
        md5_resource = response.json()['md5']
        vtreport( md5_resource)
   
#%%
#This method takes md5 resource given by API in vtscan method and checks for
#positives section in response, outputs list of files with 5 or more positives
def vtreport(resource):
    global files_to_encrypt, file_to_scan
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': '42c175b53b9749272ebe4a5019679045b8a590aeb8f1dc87c91e6ad807121d72' , 'resource': resource }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        result_positives = response.json()['positives']
        print("Positive scan result = " + str(result_positives) )
        if result_positives >= 5: #if the positives are less than 5 then it is condemned as safe
            files_to_encrypt.append(file_to_scan)
    elif response.status_code == 204:
        print("Error Code '204', VirusTotal file limit exceeded!" )
	elif response.status_code == 400:
		print("Error Code '400', Bad request. Your request was somehow incorrect.")
    else:
        print("Error Code '403', Please check VirusTotal API key" )


#%%
#This method handles timing between scan/report requests
#The Public API is limited to 4 requests per minute. 
def vt(execs):
    global file_to_scan
    execFiles = execs
    if execFiles:
        flag = 0
        for x in execFiles:
            file_to_scan = x[0]
            print("File being scanned now: " + file_to_scan)
            vtscan(x)
            flag+=1
            if (x == execFiles[len(execFiles)-1]):
                break
            if flag ==2:
                time.sleep(60)
                flag = 0
    return(files_to_encrypt)

#%%
