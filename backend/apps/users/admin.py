from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import OTPCode, User, UserAddress


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ('id', 'phone', 'role', 'is_staff')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('phone', 'password', 'role', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'role', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.register(OTPCode)
admin.site.register(UserAddress)
