from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path, include
from django.utils.html import format_html
from django.contrib import messages
from django.http import HttpResponseRedirect
from core.services import ServiceCambioEstadoPostulacionUNQ
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

    def changelist_view(self, request, extra_context=None):
        # Store the request object for use in other methods
        self.request = request
        return super().changelist_view(request, extra_context)

    def acciones(self, obj):
        # Muestro los botones si el usuario es superuser
        if hasattr(self, 'request') and self.request.user.is_superuser:
            # Si el estado es pendiente, muestro los botones
            aprobar_button = (
                '<a class="button" style="margin-right: 5px; background-color: #28a745; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none;" href="{}">'
                '&#x2714;</a>'.format('aprobar/{}'.format(obj.pk))
                if obj.estado == "p" else ""
            )
            rechazar_button = (
                '<a class="button" style="margin-left: 5px; background-color: #dc3545; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none;" href="{}">'
                '&#x2716;</a>'.format('rechazar/{}'.format(obj.pk))
                if obj.estado == "p" else ""
            )
            return format_html(aprobar_button + rechazar_button)
        return ""

    acciones.short_description = 'Acciones'

    def get_urls(self):
        """
        Añadir URL personalizada para la acción de marcar como aprobado
        """
        urls = super().get_urls()
        custom_urls = [
            path('aprobar/<int:id_postulacion>/', self.aprobar),
            path('rechazar/<int:id_postulacion>/', self.rechazar),
        ]
        return custom_urls + urls

    def get_list_display(self, request):
        # Agregar un botón en cada fila del listado
        return super().get_list_display(request) + ('acciones', )
    
    def aprobar(self, request, id_postulacion):
        previous_url = request.META['HTTP_REFERER']
        service_estados = ServiceCambioEstadoPostulacionUNQ()
        try:  
            profile = UserProfile.objects.get(user=request.user)
            postulacion = ConvocatoriaUNQPostulacion.objects.get(pk=id_postulacion)
            service_estados.aprobar(profile=profile, postulacion=postulacion) 
        except Exception as err:
            self.message_user(request, "Ocurrio un error al aprobar la solicitud : {}".format(str(err)), level=messages.ERROR)
            return HttpResponseRedirect(previous_url)
        self.message_user(request, "Se aprobó la solicitud : {}".format(str(profile)))
        return HttpResponseRedirect(previous_url)
    
    def rechazar(self, request, id_postulacion):
        previous_url = request.META['HTTP_REFERER']
        service_estados = ServiceCambioEstadoPostulacionUNQ()
        try:  
            profile = UserProfile.objects.get(user=request.user)
            postulacion = ConvocatoriaUNQPostulacion.objects.get(pk=id_postulacion)
            service_estados.rechazar(profile=profile, postulacion=postulacion) 
        except Exception as err:
            self.message_user(request, "Ocurrio un error al rechazar la solicitud : {}".format(str(err)), level=messages.ERROR)
            return HttpResponseRedirect(previous_url)
        self.message_user(request, "Se rechazó la solicitud : {}".format(str(profile)))
        return HttpResponseRedirect(previous_url)

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