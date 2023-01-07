
import socket, subprocess, threading, sys, shlex, os
import paramiko
import dotenv
from mitrecve import crawler
import nvdlib
import getpass
import asyncio , aiohttp


dotenv.load_dotenv()

socket.setdefaulttimeout(5)
apiKey = os.getenv('API_KEY')
# addressInfo = []

async def portScanner(address):
    addressInfo = []
    for port in range(1012):
      
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        check = sock.connect_ex((address,port))
        if check == 0 :
            addressInfo.append(port)
            service = None 
            try:
                service = socket.getservbyport(port)
                addressInfo.append(service)
            except:
                continue
                addressInfo.append(service)

        else:
            pass
    return(addressInfo)

async def Scanner(address, username, password):
    addressInfo = []
    systemInfo = []
    V = []
    hostname = socket.getfqdn(address)
    # addressInfo.append(hostname)

    addressInfo = (portScanner(address))
    addressInfo = await addressInfo
    await asyncio.sleep(0)

    processes , kernel  = await remoteExecution(address, username, password)
    for process in processes:
        systemInfo.append(process)
    netVulns = await getVulnerability(addressInfo)
    programvulns = await getProgramVulnerability(kernel, systemInfo)
    V =  netVulns + programvulns
    return (V) 
         
async def getVulnerability(addressInfo):
    
    netVulns = []
    for i in range(len(addressInfo)):
        if addressInfo[i] is not None:
            query = addressInfo[i-1:i]
        else:
            query = addressInfo[i]
        
        CVEs = nvdlib.searchCVE(keywordSearch= query, limit=4, key=apiKey, delay=.6)
        # CVEs = crawler.get_main_page(query)
        # for eachCVE in CVEs:
        #     if eachCVE.score[2] != 'LOW':
        #         netVulns.append(eachCVE.id)
        #     else:
        #         continue
        
        print(query)
        for eachCVE in CVEs:
            if eachCVE.score[2] != 'LOW':
                print(eachCVE.id)
                netVulns.append(eachCVE.id)
    return(netVulns)
            

async def getProgramVulnerability(kernel,systemInfo):
    vulns = []
    program = ''

    
    for i in range(0, len(systemInfo)):
        program = systemInfo[i][0]
    
        kernel = kernel[0].split("\n")
        query = (kernel, program)
       
    
    
        # CVEs = nvdlib.searchCVE(keywordSearch = query , limit = 4, key = apiKey, delay=.6)
        CVEs = nvdlib.searchCVE(keywordSearch= query,  limit=4, key=apiKey , delay=.6)
        # CVEs = crawler.get_main_page(query)
        # while i < len(CVEs)/:
        print(query)
        for eachCVE in CVEs:
            if eachCVE.score[2] != 'LOW':
                vulns.append(eachCVE.id)
            else:
                pass
            print(eachCVE.id)
    return(vulns)
       
   

async def remoteExecution(address, username, password):
    processes = []
    kernel = ''
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(address, port=22, username=username, password=password)
    getProcesses = ("ps auxc | awk -v col=11 '{print $col}'" )
    getOS = "uname"
    stdin, stdout, stderr = client.exec_command(getProcesses)

    p = (line.split("\n") for line in stdout.readlines())

    for eachProcess in p:
        if 'COMMAND' in eachProcess:
            continue
        else:
            processes.append(eachProcess)
    
    stdin,stdout, stderr = client.exec_command(getOS)
    
    for line in stdout.readlines():
        kernel = line.split("/n") 


        

    return(processes, kernel)  


def execute(address, username, password):
    threads = []
    thread = threading.Thread(target=Scanner, args=(address, username, password, ))
    thread.start()
    threads.append(thread)

    for thread in threads:
        thread.join()
    
# if __name__ == '__main__':
#     addresses = ['206.189.180.236']
#     # for address in addresses:
#     #     Scanner(address)

#     threads = []
 
#     for address in addresses:

#         thread = threading.Thread(target=Scanner, args=(address,))
#         thread.start()
#         threads.append(thread)

#         for thread in threads:
#             thread.join()
        

    