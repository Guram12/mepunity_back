from django.contrib import admin
from .models import Project ,ProjectService , ProjectImage



class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]

admin.site.register(Project, ProjectAdmin)
@admin.register(ProjectService)
class ProjectServiceAdmin(admin.ModelAdmin):
    list_display = ('name_ka',"name_en" , 'price_per_sqm', 'discount_percentage' , "dtype")