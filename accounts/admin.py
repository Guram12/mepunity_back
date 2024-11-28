from django.contrib import admin
from .models import CustomUser , Discount
from django.contrib.sites.models import Site

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'company', 'phone_number','get_discount', 'is_email_verified')
    readonly_fields = ('email', 'username', 'phone_number', 'is_email_verified', 'company', 'get_discount' ,'image' )

    def get_discount(self, obj):
        return obj.discount.discount if hasattr(obj, 'discount') else 'No Discount'
    get_discount.short_description = 'Discount'


admin.site.register(CustomUser, CustomUserAdmin)

# --------------------------------------------------------------
class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')

admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)



# --------------------------------------------------------------
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username', 'get_company', 'discount')
    fields = ('user', 'discount')
    search_fields = ('user__email',)

    def get_username(self, obj):
        return obj.user.username if hasattr(obj.user, 'username') else 'No Username'
    get_username.short_description = 'Username'


    def get_company(self, obj):
        return obj.user.company if hasattr(obj.user, 'company') else 'No Company'
    get_company.short_description = 'Company'

admin.site.register(Discount, DiscountAdmin)