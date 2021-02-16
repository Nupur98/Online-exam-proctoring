from django.contrib import admin
from .models import Candidate,Candidate_Proc

# Register your models here.
admin.site.register(Candidate)
admin.site.register(Candidate_Proc)