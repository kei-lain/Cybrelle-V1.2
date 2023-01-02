
import socket, subprocess, threading, sys, shlex, os
import paramiko
import dotenv
from mitrecve import crawler
import nvdlib
import getpass
import concurrent.futures

dotenv.load_dotenv()

socket.setdefaulttimeout(5)
apiKey = os.getenv('API_KEY')
# addressInfo = []

def Scanner(address, username, password):
    addressInfo = []
    systemInfo = []
    hostname = socket.getfqdn(address)
    # addressInfo.append(hostname)

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

            
    processes , kernel  = remoteExecution(address, username, password)
    for process in processes:
        systemInfo.append(process)
    getVulnerability(addressInfo) 
    getProgramVulnerability(kernel, systemInfo)      

def getVulnerability(addressInfo):
    
    netVulns = []
    for i in range(len(addressInfo)):
        if addressInfo[i] is not None:
            query = addressInfo[i-1:i]
        else:
            query = addressInfo[i]

        CVEs = nvdlib.searchCVE(keywordSearch= query , limit = 4 ,key = apiKey, delay=.6)
        for eachCVE in CVEs:
            if eachCVE.score[2] != 'LOW':
                netVulns.append(eachCVE.id)
            else:
                continue
        return(print(netVulns))

def getProgramVulnerability(kernel,systemInfo):
    vulns = []
    programVulns = {}
    program = ''

    
    for i in range(0, len(systemInfo)):
        program = systemInfo[i][0]
        query = (f'{program}')
        # print(query)
    
    
        CVEs = nvdlib.searchCVE(keywordSearch = query , limit = 4, key = apiKey, delay=.6)
        for eachCVE in CVEs:
            if eachCVE.score[2] != 'LOW':
                vulns.append(eachCVE.id)
            else:
                continue
        programVulns[program] = vulns
        
    return(print(programVulns))  

def remoteExecution(address, username, password):
    processes = []
    kernel = ''
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    user= username
    passwd= password
    client.connect(address, port=22, username=user, password=passwd)
    getProcesses = ("ps auxc | awk -v col=11 '{print $col}'" )
    getOS = "uname -r"
    stdin, stdout, stderr = client.exec_command(getProcesses)

    p = (line.split("\n") for line in stdout.readlines())

    for eachProcess in p:
        if 'COMMAND' in eachProcess:
            continue
        else:
            processes.append(eachProcess)
    stdin,stdout, stderr = client.exec_command(getOS)
    for kernel in stdout.readlines():
        kernel = kernel 
        

    return(processes, kernel)  


def execute(address, username, password):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future = executor.submit(Scanner,address, username, password)
        return(future.result())
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
        

    