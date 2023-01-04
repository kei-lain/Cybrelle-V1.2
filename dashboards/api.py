from ninja import NinjaAPI
from django.db import IntegrityError
import json
from typing import List
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib import admin
from .cybrelle import Scanner , execute
from .openai_integration import getCVEFix
from .models import Host, CVE, Instructions
from .schema import HostSchema , CVESchema, NotFoundSchema , InstructionsSchema



api = NinjaAPI()

@api.get("hosts/",response=List[HostSchema])
def hosts(request):
    return Host.objects.all()

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

@api.api_operation(["POST","GET"], "cves/{host_id}", response={201:CVESchema})
def cves(request,host_id: int):
    hosts = Host.objects.filter(pk=host_id)
    host_obj = get_object_or_404(Host, pk=host_id)
    host_for_cve = host_obj.hostname
    user = host_obj.user
    hostname = host_obj.hostname
    organization = host_obj.organization
    host_username = host_obj.host_username
    host_password = host_obj.host_password
    ip_address = host_obj.ip_address
    scan_results = Scanner(ip_address, host_username, host_password)
    for result in scan_results:
        try:
            new_cve = CVE.objects.create(host=host_obj, user=user, Organization=organization, cves=result)
            new_cve.save()
        except IntegrityError:
        # Handle the integrity error
            return(print('Error: null value in column "cves"'))
    return new_cve

@api.api_operation(["POST","GET"], "instructions/{cve_id}",  response={201: InstructionsSchema})
def instructions(request, cve_id: int):
    cve = CVE.objects.filter(pk=cve_id)
    cve_obj = get_object_or_404(CVE, pk=cve_id)
    cve_for_prompt = cve_obj.cves
    instruction = getCVEFix(cve=cve_for_prompt)
    new_instructions = Instructions.objects.create(cve=cve_obj , instruction=(instruction))
    new_instructions.save()
    return(new_instructions)







    
    




    

# @api.post("cves/{host_id}", response={201: CVESchema})
# def find_vulns(request, host_id: int ,cve: CVESchema): #Doing it this way allows the function to expect to get data in the same format as the schema
#     try:
#         host = Host.objects.get(pk=host_id)

#         cve = CVE.objects.create(execute(address=host.ip_address, username=host.host_username,password=host.host_password))
#         return {"message" : f"Successfully found CVE(s): {cve}"}
#     except:
#         return {"message" : "Couldn't find CVEs"}
                



    


