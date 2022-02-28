from django.contrib import admin
from .models import *
from .models import Friend, Belonging, Borrowed

admin.site.register([Friend, Belonging, Borrowed])