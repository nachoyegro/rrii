from django.db import models

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