from django.contrib import admin
from .models import CustomUser
from django.contrib.sites.models import Site

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'company', 'formatted_discount', 'phone_number', 'is_email_verified')

    def formatted_discount(self, obj):
        return f"{obj.discount} %"
    formatted_discount.short_description = 'Discount'

admin.site.register(CustomUser, CustomUserAdmin)

class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')

admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)