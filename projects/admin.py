from django.contrib import admin
from .models import Project ,ProjectService , ProjectImage, Minimum_Amount_Of_Space
from django.forms import ModelForm
from django.core.exceptions import ValidationError



class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ('title_ka', 'title_en', 'priority')
    
admin.site.register(Project, ProjectAdmin)


@admin.register(ProjectService)
class ProjectServiceAdmin(admin.ModelAdmin):
    list_display = ('name_ka', 'name_en', 'price_per_sqm_below_hotel', 'price_per_sqm_above_hotel', 'discount_percentage', 'dtype')


# ===============================================  project price admin  ==========================================
class MinimumAmountOfSpaceForm(ModelForm):
    class Meta:
        model = Minimum_Amount_Of_Space
        fields = '__all__'

    def clean(self):
        if not self.instance.pk and Minimum_Amount_Of_Space.objects.exists():
            raise ValidationError('There can be only one instance of Minimum_Amount_Of_Space. მეტი არ დაამატო :დ')
        return super().clean()

class MinimumAmountOfSpaceAdmin(admin.ModelAdmin):
    form = MinimumAmountOfSpaceForm

admin.site.register(Minimum_Amount_Of_Space, MinimumAmountOfSpaceAdmin)
    










