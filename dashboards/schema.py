from ninja import Schema, ModelSchema
from .models import CVE , Report, Host
from typing import List
from pydantic import validator, BaseModel
import concurrent.futures
import asyncio


class HostSchema(Schema):
    #Needs to match field names exactly
    ip_address: str
    host_username: str
    host_password: str
    host_id: int

    def __str__(self):
        self.ip_address

class NotFoundSchema(Schema):
    message: str


class CVESchema(Schema):
    host : int
    cves: str
    info: str

    @validator("host")


    def validate_host(cls, host):
        async def check_host():
            if host is int:
                return host
            else:
                print("Host incorrect")
        pool = concurrent.futures.ThreadPoolExecutor(1)
        result = pool.submit(asyncio.run, check_host()).result()
        return result

    # @staticmethod
    # def resolve_host(obj):
    #     if obj.host is  int:
    #         return
    #     return(f'{obj.Host.id}')
   

    
   
    # @staticmethod
    # def set_host(self,obj):
    #     if not obj.host:
    #         return
    #     return f"{obj.host.hostname}"
        


class ReportSchema(ModelSchema):
    class Config:
        model = Report
        model_fields = '__all__'



class Error(Schema):
    message: str
    