from django.contrib import admin

class SistemaRRIISite(admin.AdminSite):
    def get_app_list(self, request, app_label=None):
        apps = super().get_app_list(request, app_label)
        config_new_app_proxy = {} 
        for app in apps:
            # Obtengo los modelos registrados de la app y si es el modelo core aplico un ordenamiento
            if app["name"] == "Administración UNQ":
                # Creo una app fiticia para agrupar los modelos relacionados a docentes
                models_core, models_administracion = self._get_modelos_separados_por_app(app['models']) 
                config_new_app_proxy["name"] = "Base de datos"
                config_new_app_proxy["app_label"] = "administracion"
                config_new_app_proxy["app_url"] = app["app_url"]
                config_new_app_proxy["has_module_perms"] = app["has_module_perms"]
                config_new_app_proxy["models"] = models_administracion
                app['models'] = models_core
        apps.append(config_new_app_proxy)
        return apps
    
    def _get_modelos_separados_por_app(self, modelos):
        modelos_de_administracion = {
            "ConvocatoriaExternaSolicitud": ""
        }
        modelos_core = []
        modelos_administracion = []
        for modelo in modelos:
            if modelo['model'].__name__ in modelos_de_administracion:
                modelos_administracion.append(modelo)
            else:
                modelos_core.append(modelo)
        return modelos_core, modelos_administracion

sistema_rrii_site = SistemaRRIISite()