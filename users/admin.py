from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'email', 'is_staff', 'is_active')
    search_fields = ('user_name', 'email')
    list_filter = ('is_staff', 'is_active')
