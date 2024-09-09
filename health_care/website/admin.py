from django.contrib import admin
from .models import CustomUser,Medicine,Doctor,Department

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    # Add any other configurations here
class Medicineadmin(admin.ModelAdmin):
    model = Medicine

class Doctoradmin(admin.ModelAdmin):
    model = Doctor

class Departmentadmin(admin.ModelAdmin):
    model = Department

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Medicine,Medicineadmin)
admin.site.register(Doctor,Doctoradmin)
admin.site.register(Department,Departmentadmin)