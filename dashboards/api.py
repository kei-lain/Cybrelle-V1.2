from ninja import NinjaAPI
from django.db import IntegrityError
from django.forms.models import model_to_dict
from asgiref.sync import sync_to_async
import json
import asyncio
import threading
import nvdlib
from mitrecve import crawler
from typing import List
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib import admin
from .cybrelle import Scanner , reportGen
from .openai_integration import getCVEFix
from .models import Host, CVE, Report
from django.core.serializers import serialize
from .schema import HostSchema , CVESchema, NotFoundSchema , ReportSchema
import dotenv, os

dotenv.load_dotenv(".env")
apiKey = os.getenv('API_KEY')
api = NinjaAPI()


@api.get("hosts/{host_id}", response={200: HostSchema, 404: NotFoundSchema})
def host(request, host_id: int):
    try:
        host = Host.objects.get(pk=host_id)
        return 200, host

    except Host.DoesNotExist as e:
        return 404, {"message": "Host does not exist"}

@api.post("hosts/", response={201: HostSchema})
def create_host(request, host: HostSchema):
    host = Host.objects.create(**host.dict())
    return host
@api.get("cves/", response=List[CVESchema])
def cves(request):
    return  CVE.objects.all()


@api.api_operation(["POST","GET"], "cves/{host_id}", response={201:CVESchema, 201:ReportSchema})
async def cves(request,host_id: int):
    threads = []
    sections = []
    hosts = Host.objects.filter(pk=host_id)
    host_obj = await sync_to_async(get_object_or_404)(Host, pk=host_id)
    # user =  sync_to_async(lambda: host_obj.user)
    
    hostname = host_obj.hostname
    # organization = sync_to_async(lambda: host_obj.organization)
   
    host_username = host_obj.host_username
    host_password = host_obj.host_password
    ip_address = host_obj.ip_address
    report = await (reportGen(ip_address, host_username, host_password))
    futures  = asyncio.ensure_future(Scanner(ip_address, host_username, host_password))
    report = report
    for key in report:
        section = report[key]
        sections.append(section)

    # futures = await asyncio.gather(Scanner(ip_address,host_username, host_password))
    new_report = await sync_to_async(Report.objects.create)(host=host_obj, report=sections)
    for future in asyncio.as_completed([futures]):

        results = await future

        
        for result in results:
            result = str(result)
            
           
            details = crawler.get_main_page(result)
            for n in range(len(details)):
                detail = details[n]['DESC']
            
            try:
                print(result)
                new_cve= await sync_to_async(CVE.objects.create)(host=host_obj,cves=result, info=detail)


            except TimeoutError:
                continue

            
                # await sync_to_async(new_cve.save())
            except IntegrityError:
            # Handle the integrity error
                return(print('Error: null value in column "cves"'))
    
   
    return new_cve, new_report


@api.get("reports/{host_id}", response={200: ReportSchema})
def reports(request, host_id: int):
    host = Host.objects.get(pk=host_id)
    reports = Report.objects.all().filter(host=host)

    return 200, reports




# @api.get("cves/get/{host_id}" , response={200: CVESchema} )
# def getCVES(request, host_id : int):
#     cve = CVE.objects.all().filter(pk=host_id)

#     return  200, cve

    # for cve in cves:
    #     json_data = serialize('json', cve)
    #     return json_data
    
# @api.api_operation(["POST","GET"], "instructions/{cve_id}",  response={201: InstructionsSchema})
# def instructions(request, cve_id: int):
#     cve = CVE.objects.filter(pk=cve_id)
#     cve_obj = get_object_or_404(CVE, pk=cve_id)
#     cve_for_prompt = cve_obj.cves
#     instruction = getCVEFix(cve=cve_for_prompt)
#     new_instructions = Instructions.objects.create(cve=cve_obj , instruction=(instruction))
#     new_instructions.save()
#     return(new_instructions)







    
    




    

# @api.post("cves/{host_id}", response={201: CVESchema})
# def find_vulns(request, host_id: int ,cve: CVESchema): #Doing it this way allows the function to expect to get data in the same format as the schema
#     try:
#         host = Host.objects.get(pk=host_id)

#         cve = CVE.objects.create(execute(address=host.ip_address, username=host.host_username,password=host.host_password))
#         return {"message" : f"Successfully found CVE(s): {cve}"}
#     except:
#         return {"message" : "Couldn't find CVEs"}
                



    


