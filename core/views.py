from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import View

class SolicitudAlumnoAprobarView(View):
        @method_decorator(user_passes_test(lambda u: u.is_superuser))
        def get(self, request):
            print('Hola')
            #return render(request, self.get_template(), dict(form=form, report=report, processing=True))