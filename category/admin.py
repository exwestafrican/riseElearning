from django.contrib import admin
from .models import CourseCategory
# Register your models here.

class CourseCategoryAdmin(admin.ModelAdmin):
    readonly_fields =['slug']

admin.site.register(CourseCategory,CourseCategoryAdmin)