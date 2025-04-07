from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path, include
from core.models import *
from core.views import *

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
        universidad = UserProfile.objects.get(user=request.user).universidad
        if not request.user.is_superuser and db_field.name == "universidad":
            kwargs["queryset"] = Universidad.objects.filter(pk=universidad.pk) #Hago esto para transformarlo en queryset
        if not request.user.is_superuser and db_field.name == "alumno":
            kwargs["queryset"] = Alumno.objects.filter(universidad=universidad)  #Hago esto para transformarlo en queryset
        return super(FiltradoUniversidadAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
 
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

class UniversidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', )

class CarreraAdmin(admin.ModelAdmin):
    list_display = ('universidad', 'nombre', )

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline,]

class AlumnoAdmin(FiltradoUniversidadAdmin):
    list_display = ('legajo', 'apellido', 'nombre', 'universidad')

class ConvocatoriaUNQUniversidadInline(admin.TabularInline):
    model = ConvocatoriaUNQUniversidad
    extra = 0

class ConvocatoriaUNQAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'anio', 'plazas', 'activa')
    filter_horizontal = ('carreras',)
    inlines = [ConvocatoriaUNQUniversidadInline,]

class ConvocatoriaUNQPostulacionAdmin(FiltradoUniversidadAdmin):
    list_display = ('convocatoria', 'alumno', 'estado')
    exclude = ('estado', )

    def get_queryset(self, request):
        qs = super(FiltradoUniversidadAdmin, self).get_queryset(request)
        # Si el usuario es SuperUsuario, puede ver el queryset completo
        if request.user.is_superuser:
            return qs
        # Sino, filtro el queryset en base a su universidad asignada
        profile = UserProfile.objects.get(user=request.user)
        return qs.filter(alumno__universidad=profile.universidad)

class ConvocatoriaExternaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'universidad', 'anio', 'activa')

class ConvocatoriaExternaSolicitudAdmin(admin.ModelAdmin):
    list_display = ('convocatoria', 'alumno', 'estado')
    readonly_fields = ('estado',)

    def get_urls(self):
        urls = super().get_urls()
        nuevas_urls = [ path(r'^(.+)/aprobar/$', self.admin_site.admin_view(self.aprobar),
                name='aprobar_view'),
                ]
        return nuevas_urls + urls
    
    def aprobar(self, request):
        print('Aprobado mostro')

    """
    ### ESTO SOLO SERVIA CUANDO LAS CONVOCATORIAS ESTABAN UNIFICADAS.
    # Solo muestro las solicitudes de la universidad correspondiente al usuario actual
    def get_queryset(self, request):
        qs = super(ConvocatoriaExternaSolicitudAdmin, self).get_queryset(request)
        # Si el usuario es SuperUsuario, puede ver el queryset completo
        if request.user.is_superuser:
            return qs
        # Sino, filtro el queryset en base a su universidad asignada
        profile = UserProfile.objects.get(user=request.user)
        return qs.filter(alumno__universidad=profile.universidad)

    # Filtro los campos del form en base a la universidad
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filtro los alumnos del form
        if not request.user.is_superuser:
            if db_field.name == "alumno":
                universidad = UserProfile.objects.get(user=request.user).universidad
                kwargs["queryset"] = Alumno.objects.filter(universidad=universidad)  #Hago esto para transformarlo en queryset
            if db_field.name == "convocatoria":
                # Si el usuario es externo, solo muestro las convocatorias de UNQ
                kwargs["queryset"] = ConvocatoriaExterna.objects.filter(universidad__sigla='UNQ') 
        # TODO: filtrar convocatorias segun corresponda al perfil de usuario
        return super(ConvocatoriaExternaSolicitudAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    """

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Universidad, UniversidadAdmin)
admin.site.register(Carrera, CarreraAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(ConvocatoriaExterna, ConvocatoriaExternaAdmin)
admin.site.register(ConvocatoriaExternaSolicitud, ConvocatoriaExternaSolicitudAdmin)
admin.site.register(ConvocatoriaUNQ, ConvocatoriaUNQAdmin)
admin.site.register(ConvocatoriaUNQPostulacion, ConvocatoriaUNQPostulacionAdmin)

admin.site.site_header = "Relaciones Internacionales"
admin.site.site_title = "Relaciones Internacionales"
admin.site.index_title = "Relaciones Internacionales"