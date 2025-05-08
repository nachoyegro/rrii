class ServiceCambioEstadoPostulacionUNQ():

    def aprobar(self, profile, postulacion):
        """
        Cambia el estado de la postulacion a 'Aprobado'
        """
        try:
            # Cambia el estado de la postulacion a 'Aprobado'
            postulacion.estado = 'a'
            postulacion.save()
        except Exception as err:
            raise Exception("Error al aprobar la postulacion: {}".format(str(err)))

    def rechazar(self, profile, postulacion):
        """
        Cambia el estado de la postulacion a 'Aprobado'
        """
        try:
            # Cambia el estado de la postulacion a 'Aprobado'
            postulacion.estado = 'r'
            postulacion.save()
        except Exception as err:
            raise Exception("Error al rechazar la postulacion: {}".format(str(err)))