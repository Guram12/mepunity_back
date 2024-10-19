from django.contrib import admin
from .models import Project ,ProjectService



admin.site.register(Project)


@admin.register(ProjectService)
class ProjectServiceAdmin(admin.ModelAdmin):
    list_display = ('name_ka',"name_en" , 'price_per_sqm', 'discount_percentage' , "dtype")