from django.contrib import admin
from django.core import validators
from .models import User

class UserAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de registros en el admin
    list_display = ('username', 'name', 'email', 'is_active')

    # # Campos que se mostrarán en la página de detalles del registro en el admin
    # fields = ('username', 'name', 'email', 'is_active')
    # O puedes usar fieldsets para agrupar los campos en secciones
    fieldsets = (
        ('Información Personal', {'fields': ('username', 'name', 'email')}),
        ('Estado', {'fields': ('is_active','is_staff',)}),
    )
    exclude = ('date_joined',)

admin.site.register(User, UserAdmin)
