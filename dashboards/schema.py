from ninja import Schema, ModelSchema
from .models import CVE


class HostSchema(Schema):
    #Needs to match field names exactly
    ip_address: str
    host_username: str
    host_password: str

    def __str__(self):
        self.ip_address

class NotFoundSchema(Schema):
    message: str


class CVESchema(ModelSchema):
    class Config:
        model = CVE
        model_fields = '__all__'