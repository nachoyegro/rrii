from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import *

class FiltradoUniversidadAdmin(admin.ModelAdmin):
    exclude = ['user',]

    def get_queryset(self, request):
        qs = super(FiltradoUniversidadAdmin, self).get_queryset(request)
        # Si el usuario es SuperUsuario, puede ver el queryset completo
        if request.user.is_superuser:
            return qs
        # Sino, filtro el queryset en base a su universidad asignada
        profile = UserProfile.objects.get(user=request.user)
        return qs.filter(universidad=profile.universidad)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "universidad":
            universidad = UserProfile.objects.get(user=request.user).universidad
            kwargs["queryset"] = Universidad.objects.filter(pk=universidad.pk) #Hago esto para transformarlo en queryset
        return super(FiltradoUniversidadAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
 
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

class UniversidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', )

class CarreraAdmin(admin.ModelAdmin):
    list_display = ('universidad', 'nombre', )

class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('carrera', 'nombre')

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('carrera', 'nombre')

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline,]

class AlumnoAdmin(FiltradoUniversidadAdmin):
    list_display = ('legajo', 'apellido', 'nombre', 'universidad')

class SolicitudAlumnoAdmin(admin.ModelAdmin):
    list_display = ('convocatoria', 'alumno')

    # Solo muestro las solicitudes de la universidad correspondiente al usuario actual
    def get_queryset(self, request):
        qs = super(SolicitudAlumnoAdmin, self).get_queryset(request)
        # Si el usuario es SuperUsuario, puede ver el queryset completo
        if request.user.is_superuser:
            return qs
        # Sino, filtro el queryset en base a su universidad asignada
        profile = UserProfile.objects.get(user=request.user)
        return qs.filter(alumno__universidad=profile.universidad)

    # Filtro los campos del form en base a la universidad
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filtro los alumnos del form
        if not request.user.is_superuser and db_field.name == "alumno":
            universidad = UserProfile.objects.get(user=request.user).universidad
            kwargs["queryset"] = Alumno.objects.filter(universidad=universidad) #Hago esto para transformarlo en queryset
        # TODO: filtrar convocatorias segun corresponda al perfil de usuario
        return super(SolicitudAlumnoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Universidad, UniversidadAdmin)
admin.site.register(Carrera, CarreraAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(SolicitudAlumno, SolicitudAlumnoAdmin)
admin.site.register(Convocatoria)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.site_header = "Relaciones Internacionales"
admin.site.site_title = "Relaciones Internacionales"
admin.site.index_title = "Relaciones Internacionales"