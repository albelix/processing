from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse

from .models import Upload

class UploadView(CreateView):
    model = Upload
    fields = ['upload_file', ]
    success_url = reverse_lazy('fileupload')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Upload.objects.all()
        return context

class PythonScript(CreateView):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.POST = None
        self.method = None

    def run(request):
        if request.method == 'POST' and 'run_script' in request.POST:
            # import function to run
            import os
            import django
            from management.commands.main_scriptfile import run
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "processing.settings")
            django.setup()

            outcome = run()

            # return user to required page
            return HttpResponse(outcome)
        #    return HttpResponseRedirect(reverse('upload_form'))
