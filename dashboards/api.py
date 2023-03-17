from ninja import NinjaAPI

from ninja.responses import codes_2xx
import pydantic
from ninja.errors import HttpError , ValidationError, ConfigError
from django.db import IntegrityError
from django.forms.models import model_to_dict
from asgiref.sync import sync_to_async
import json
import asyncio
import threading
import stripe
import nvdlib
from mitrecve import crawler
from ninja.pagination import paginate
from typing import List
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib import admin
from .cybrelle import Scanner , reportGen
from .models import Host, CVE, Report
from django.core.serializers import serialize
from .schema import HostSchema , CVESchema, NotFoundSchema , ReportSchema, Error
import dotenv, os
import asyncio
from django.contrib.auth.decorators import login_required
from ninja.openapi.views import openapi_json
from ninja.security import APIKeyHeader, django_auth

dotenv.load_dotenv(".env")
apiKey = os.getenv('API_KEY')
api = NinjaAPI(openapi_url=None)


# class ApiKey(APIKeyHeader):
#     param_name = "X-API-Key"

#     def authenticate(self, request, key):
#         if key == os.getenv('Cybrelle_API_KEY'):
#             return key


# header_key = ApiKey()


stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY

@login_required
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

@login_required
@api.api_operation(["POST","GET"], "cves/{host_id}", response={codes_2xx:  CVESchema ,201: ReportSchema, 500: Error})
async def cves(request,host_id: int):
    threads = []
    sections = []
    new_cve = ''
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
    report = report  ##report generation works
    for key in report:
        section = report[key]
        sections.append(section)

    # futures = await asyncio.gather(Scanner(ip_address,host_username, host_password))
    new_report = await sync_to_async(Report.objects.create)(host=host_obj, report=sections) 
    for future in asyncio.as_completed([futures]):

        results = await future

        
        for result in results:
            result = str(result)
            print(result)
        
            try:
                details = (crawler.get_main_page(result))
                if len(details) >= 1:
                    detail = details[0]['DESC']
                else:
                    detail = result
                

                new_cve= await sync_to_async(CVE.objects.create)(host_id=host_obj.id,cves=str(result), info=detail)
            
            except ValidationError as e:
                print(e)
                
            except ConfigError as e:
                print(e)
                

            except pydantic.ValidationError as e:
                print(e)
                

            except TimeoutError:
                print(TimeoutError())
            except ValueError as e:
                print(e)
            
            
                # await sync_to_async(new_cve.save())
            except IntegrityError:
            # Handle the integrity error
                return(print('Error: null value in column "cves"'))
            
    
   
    return 201, new_cve, 

@login_required
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
                



    


