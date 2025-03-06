# Register your models here.
from django.contrib import admin
from .models import Family, Insuree, TblInsuree

admin.site.register(Family)
admin.site.register(Insuree)
admin.site.register(TblInsuree)
