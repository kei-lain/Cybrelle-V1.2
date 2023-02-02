
import socket, subprocess, threading, sys, shlex, os, platform
import paramiko
import dotenv
import distro
from mitrecve import crawler
import nvdlib
import getpass
import asyncio , aiohttp
import openai , requests
from requests.exceptions import HTTPError



socket.setdefaulttimeout(5)

dotenv.load_dotenv()

apiKey = os.getenv('API_KEY')
openai.api_key = os.getenv('OPEN_AI_API_KEY')
api_endpoint = "https://api.openai.com/v1/completions"
# addressInfo = []

async def portScanner(address):
    addressInfo = []
    for port in range(1,60000):
      
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
    unitVulns= await systemdScanner(address, username, password)

    V = unitVulns + netVulns + programvulns
    
    return(list(V)) 
         
async def getVulnerability(addressInfo):
    
    netVulns = []
    for i in range(len(addressInfo)):
        if addressInfo[i] is not None:
            # query = addressInfo[i-1:i]
            # query = (query)
            query1 = (f'{addressInfo[i-1]}')
            quer2 = (f'{addressInfo[i]}')
            CVEs = crawler.get_main_page(query1 + query1)
        else:
            query = addressInfo[i]
            CVEs = crawler.get_main_page(query)
        
       
        
        # CVEs = nvdlib.searchCVE(keywordSearch= query, limit=4, key=apiKey, delay=.6)
        # for eachCVE in CVEs:
        #     print(eachCVE.id)
        #     netVulns.append(eachCVE)
        for v in CVEs:
            ID = CVEs[v]['ID']
            
            netVulns.append(ID)

        #     if eachCVE.score[2] != 'LOW':
        #         netVulns.append(eachCVE.id)
        #     else:
        #         continue
       
       
    return(netVulns)
            

async def getProgramVulnerability(kernel,systemInfo):
    vulns = []
    program = ''
    kernel[0].split("\n")
    print(kernel)

    
    for i in range(0, len(systemInfo)):
        program = systemInfo[i]
        print(program)
        query = []
        
        
        # kernel = kernel.split("\n")
        query1 = (f'{kernel}')
        query2 = (f'{program}')
        print(query1, query2)
    
    
        # CVEs = nvdlib.searchCVE(keywordSearch = query , limit = 4, key = apiKey, delay=.6)
        # CVEs = nvdlib.searchCVE(keywordSearch= query,  limit=4, key=apiKey , delay=.6)
        CVEs = crawler.get_main_page(query1 + query2)
        # while i < len(CVEs)/:
        print(query)
        for v in CVEs:
            if query2 in CVEs[v]['DESC']:
                ID= (CVEs[v]['ID'])
            

                vulns.append(ID)
                print(ID)
        
        # for eachCVE in CVEs:
        #     if eachCVE.score[2] != 'LOW':
        #         vulns.append(eachCVE.id)
        #     else:
        #         pass

    return(vulns)
       
   

async def remoteExecution(address, username, password):
    programs = []
    kernel = ''
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(address, port=22, username=username, password=password)
    # getProcesses = ("ps auxc | awk -v col=11 '{print $col}'" )
    getOperatingSysyem = ("lsb_release -is")
    stdin, stdout, stderr = client.exec_command(getOperatingSysyem)
    
    operatingSystem = stdout.readline()
    print(operatingSystem)
    
       
    
    if operatingSystem.__contains__("CentOS") or operatingSystem.__contains__("Fedora") or operatingSystem.__contains__("Red Hat"):
        getPrograms = ("rpm -qa | awk '{print $1}'")
        stdin, stdout, stderr = client.exec_command(getPrograms)
        print("Red Hat Based")
    elif operatingSystem.__contains__('Ubuntu') or operatingSystem.__contains__('Debian'):
        getPrograms = ("apt list --installed")
        stdin, stdout, stderr = client.exec_command(getPrograms)
        print("Debian based")
    elif operatingSystem.__contains__('Arch'):
        getPrograms = ("pacman -Q")
        stdin, stdout, stderr = client.exec_command(getPrograms)
        print("Arch based")
    else:
        getPrograms = ("zypper search -i")
        stdin, stdout, stderr = client.exec_command(getPrograms)
        
    
    



        # try:
           
        #    getPrograms = ("Get-WMIObject -Query "SELECT * FROM Win32_Product" | FT")
        #    stdin, stdout, stderr = client.exec_command(getPrograms)
        # except:
        #    print ("Cannot get the listg of programs for this windows machine")
    for eachProgram in stdout.readlines():
        print(eachProgram)
        programs.append(eachProgram)
    
    getOS = ("uname")
    stdin, stdout, stderr = client.exec_command(getOS)

    for line in stdout.readlines():
        kernel = line.split("/n") 


        
    processes = programs
    return(processes, kernel)  



async def reportGen(address,username,password):
    greatConfig = await readConfigs(address, username, password)  
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(address, port=22, username=username, password=password)
    report = {}
    for config in greatConfig:
        print(config)
        getContents = (f"cat {config}")
        stdin, stdout, stderr = client.exec_command(getContents)
        configInfo = stdout.readlines()
        print(configInfo)


        prompt = (f'Can you explain if {config} is secure. If not please summarize and generate a report explaining how to fix all the issues:  {configInfo}. If {config} is not important, please skip over. Leave a new line space after writing')
        # response = requests.post(api_endpoint, json=payload, headers={"Authorization": f"Bearer {openai.api_key}"})
        # completed_text = response.json()
        try:
            response = openai.Completion.create(engine = 'text-davinci-003', prompt= prompt , max_tokens = 3000, temperature = 0.5, top_p =1 , frequency_penalty=0, presence_penalty=0)
        except:
            pass
        if 'choices' in response:
            completed_text = response['choices'][0]['text']

        else:
            completed_text = response
        report[config] = completed_text
    return(report)

    
async def systemdScanner(address,username,password):
    units = []
    unitVulns = []
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(address, port=22, username=username, password=password)
    getUnits = ("systemctl list-unit-files --type=service --all | awk '{print $1}'")
    stdin, stdout, stderr = client.exec_command(getUnits)
    for eachUnit in stdout.readlines():
        print(eachUnit)
        units.append(eachUnit)
    
    for unit in units:
        CVEs = crawler.get_main_page(unit)

        for v in CVEs:
            if CVEs[v]['DESC'].__contains__(unit):
                ID= (CVEs[v]['ID'])
                print(ID)
                unitVulns.append(ID)
    
    return(unitVulns)

async def readConfigs(address, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(address, port=22, username=username, password=password)
    listConfigs = ("find /etc -name *.conf")
    stdin, stdout, stderr = client.exec_command(listConfigs)
    configs = stdout.readlines()
    print(configs)

    
    
    return(configs)



    
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
        

    