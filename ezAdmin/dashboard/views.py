from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from user.models import UserPreferences
import markdown
import os


# Create your views here.

class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

class DocumentationView(View):
    template_name = 'dashboard/guideline.html'

    def get(self, request, *args, **kwargs):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        markdown_file_path = os.path.join(base_path, 'README.md')

        with open(markdown_file_path, 'r') as markdown_file:
            markdown_content = markdown_file.read()

        rendered_content = markdown.markdown(markdown_content)

        return render(request, self.template_name, {'rendered_content': rendered_content})

def permission_denied_view(request, exception):
    return render(request, 'dashboard/permission_denied_error.html', status=403)

def generic_error_view(request, exception=None):
    return render(request, 'dashboard/generic_error.html', status=500)

def not_found_error_view(request, exception=None):
    return render(request, 'dashboard/not_found_error.html', status=404)


class UpdateDarkModeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_preferences, created = UserPreferences.objects.get_or_create(user=request.user)
            return JsonResponse({'dark_mode': user_preferences.dark_mode})
        else:
            return JsonResponse({'dark_mode': False})
            
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_preferences, created = UserPreferences.objects.get_or_create(user=request.user)
            user_preferences.dark_mode = request.POST.get('dark_mode', False)
            user_preferences.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False}, status=403)