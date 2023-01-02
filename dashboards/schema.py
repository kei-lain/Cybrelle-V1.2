from ninja import Schema


class HostSchema(Schema):
    #Needs to match field names exactly
    ip_address: str
    host_username: str
    host_password: str

    def __str__(self):
        self.ip_address

class NotFoundSchema(Schema):
    message: str


class CVESchema(Schema):
    host: HostSchema
    cves: str