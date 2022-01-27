from django.contrib import admin
from .models import Department, Course, Module, Group, Exam, Grade

class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module)
admin.site.register(Group)
admin.site.register(Exam)
admin.site.register(Grade)
