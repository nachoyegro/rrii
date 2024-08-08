from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

class Universidad(models.Model):
    nombre = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "Universidades"    

    def __str__(self):
        return "%s" % (self.nombre)    

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

class Materia(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, blank=True, null=True)
    programa = models.ForeignKey(Programa, on_delete=models.SET_NULL, blank=True, null=True)
    nombre = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "Materias"    

    def __str__(self):
        return "%s" % (self.nombre)    

# TODO: diferenciar alumnos unq y extranjeros
class Alumno(models.Model):
    nombre = models.CharField(max_length=128)
    apellido = models.CharField(max_length=128)
    legajo = models.CharField(max_length=32)
    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s - %s, %s' % (self.legajo, self.apellido, self.nombre)

# TODO: diferenciar entre convocatorias propias y extranjeras
class Convocatoria(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, blank=True, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, blank=True, null=True)
    anio = models.IntegerField(verbose_name="Año")
    descripcion = HTMLField()

    def __str__(self):
        return '%s - %s - %d' % (self.universidad, self.carrera, self.anio)

# TODO: modelar estados
class SolicitudAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.SET_NULL, blank=True, null=True)
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.SET_NULL, blank=True, null=True)


class UserProfile(models.Model):  
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'Perfil de usuario de: %s' % (self.user.username)

    def __str__(self):
        return 'Perfil de usuario de: %s' % (self.user.username)