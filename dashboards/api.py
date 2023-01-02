from ninja import NinjaAPI
from typing import List
from django.conf import settings
from django.contrib import admin
from .cybrelle import Scanner , execute
from .models import Host, CVE
from .schema import HostSchema , CVESchema, NotFoundSchema
import concurrent.futures


api = NinjaAPI()

@api.get("hosts/",response=List[HostSchema])
def hosts(request):
    return Host.objects.all()

@api.get("hosts/{host_id}", response={200: HostSchema, 404: NotFoundSchema})
def host(request, host_id: int):
    try:
        ip = Host.objects.get(pk=host_id)
        return 200, ip

    except Host.DoesNotExist as e:
        return 404, {"message": "Host does not exist"}

# @api.get("cves/", response=List[CVESchema])
# def cves(request):
#     return  CVE.objects.all()

# @api.post("cves/{host_id}", response={201: CVESchema})
# def find_vulns(request, host_id: int ,cve: CVESchema): #Doing it this way allows the function to expect to get data in the same format as the schema
#     try:
#         host = Host.objects.get(pk=host_id)

#         cve = CVE.objects.create(execute(address=host.ip_address, username=host.host_username,password=host.host_password))
#         return {"message" : f"Successfully found CVE(s): {cve}"}
#     except:
#         return {"message" : "Couldn't find CVEs"}
                



    


