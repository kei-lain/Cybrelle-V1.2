from ninja import Schema, ModelSchema
from .models import CVE , Report


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


class CVESchema(ModelSchema):
    class Config:
        model = CVE
        model_fields = '__all__'

class ReportSchema(ModelSchema):
    class Config:
        model = Report
        model_fields = '__all__'
    