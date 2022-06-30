from django.contrib import admin

from users.models import AdvUser


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__', )
    search_fields = ('email',)
    fields = (
        ('email',),
        ('is_active', ),
        ('is_staff', 'is_superuser'),
        ('groups', 'user_permissions'),
    )


admin.site.register(AdvUser, AdvUserAdmin)
