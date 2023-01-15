from dashboards.models import CVE
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib import admin

CVE.object.all().delete()
