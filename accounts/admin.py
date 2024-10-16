from django.contrib import admin
from .models import CustomUser
from django.contrib.sites.models import Site


admin.site.register(CustomUser)




class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name') 


admin.site.unregister(Site)  
admin.site.register(Site, SiteAdmin) 






