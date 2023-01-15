from django.contrib import admin
from .models import Host , CVE, Report

admin.site.register(Host)
admin.site.register(CVE)
# Register your models here.
admin.site.register(Report)
