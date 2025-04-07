from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

class Universidad(models.Model):
    nombre = models.CharField(max_length=128)
    sigla = models.CharField(max_length=12)

    class Meta:
        verbose_name_plural = "Universidades"    

    def __str__(self):
        return "%s" % (self.sigla)    

class Carrera(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, blank=True, null=True)
    nombre = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "Carreras"    

    def __str__(self):
        return "%s" % (self.nombre)    

class Programa(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, blank=True, null=True)
    nombre = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "Programas"    

    def __str__(self):
        return "%s" % (self.nombre)    

# TODO: diferenciar alumnos unq y extranjeros
class Alumno(models.Model):
    nombre = models.CharField(max_length=128)
    apellido = models.CharField(max_length=128)
    legajo = models.CharField(max_length=32)
    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Alumnos"    

    def __str__(self):
        return '%s - %s, %s' % (self.legajo, self.apellido, self.nombre)

# Convocatoria de la UNQ para las universidades de afuera
class ConvocatoriaUNQ(models.Model):
    nombre = models.CharField(max_length=128)
    carreras = models.ManyToManyField(Carrera) # Carreras de UNQ
    anio = models.IntegerField(verbose_name="Año")
    activa = models.BooleanField(default=False)
    #descripcion = HTMLField()
    descripcion = models.TextField(blank=True, null=True)
    plazas = models.IntegerField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        verbose_name = "Convocatoria UNQ"
        verbose_name_plural = "Convocatorias UNQ"    

    def __str__(self):
        return '%s - %d' % (self.nombre, self.anio)
    
# Inline indicando que universidad participa de esa convocatoria hacia la UNQ y cuantas plazas se le aplicaron.
# El numero de plazas se utilizara para validar cuantos alumnos inscribe    
class ConvocatoriaUNQUniversidad(models.Model):
    convocatoria = models.ForeignKey(ConvocatoriaUNQ, on_delete=models.CASCADE)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    plazas = models.IntegerField()

    class Meta:
        verbose_name = "Universidad de convocatoria UNQ"
        verbose_name_plural = "Universidades de convocatoria UNQ"    

    def __str__(self):
        return '%s - %s' % (self.convocatoria, self.universidad)
    
# Instanciado por la persona encargada de crear postulaciones desde otra universidad.
# Los alumnos que puede ver son los filtrados por su propia universidad
# El alumno ya tiene universidad, por ende la relacion Postulacion-Universidad pasa a traves del alumno
class ConvocatoriaUNQPostulacion(models.Model):
    convocatoria = models.ForeignKey(ConvocatoriaUNQ, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    estado = models.CharField(choices=(('p', 'Pendiente'), ('a', 'Aprobado'), ('r', 'rechazado')), max_length=1, default='p')

    class Meta:
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones UNQ"    

    def __str__(self):
        return '%s - %s' % (self.convocatoria, self.alumno)

# Convocatoria a la que aplican los alumnos UNQ
class ConvocatoriaExterna(models.Model):
    nombre = models.CharField(max_length=128)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    anio = models.IntegerField(verbose_name="Año")
    activa = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True, null=True)
    plazas = models.IntegerField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        verbose_name_plural = "Convocatorias Externas"    

    def __str__(self):
        return '%s  - %s - %d' % (self.nombre, self.universidad, self.anio)
    
# Esta es la convocatoria a la que aplica el alumno UNQ
class ConvocatoriaExternaSolicitud(models.Model):
    convocatoria = models.ForeignKey(ConvocatoriaExterna, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE) #Filtrados por alumnos UNQ
    descripcion = models.TextField(blank=True, null=True) # Lo que puso en el formulario, puede reemplazarse por todos los datos separados
    estado = models.CharField(choices=(('p', 'Pendiente'), ('a', 'Aprobado'), ('r', 'rechazado')), max_length=1, default='p')

    class Meta:
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones Externas"    

    def __str__(self):
        return '%s  - %s - %s' % (self.convocatoria, self.alumno, self.universidad)

class UserProfile(models.Model):  
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    alumno = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Perfil de usuario de: %s' % (self.user.username)

    def __str__(self):
        return 'Perfil de usuario de: %s' % (self.user.username)