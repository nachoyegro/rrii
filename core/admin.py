from django.contrib import admin
from core.models import *

class UniversidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', )

class CarreraAdmin(admin.ModelAdmin):
    list_display = ('universidad', 'nombre', )

class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('carrera', 'nombre')

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('carrera', 'nombre')


admin.site.register(Universidad, UniversidadAdmin)
admin.site.register(Carrera, CarreraAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.site_header = "Relaciones Internacionales"
admin.site.site_title = "Relaciones Internacionales"
admin.site.index_title = "Relaciones Internacionales"