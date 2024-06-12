import django.views as django_views
import django.http as django_http
import django.views.decorators.csrf as django_views_csrf


class HomeView(django_views.View):
    @django_views_csrf.csrf_exempt
    def get(self, request):
        return django_http.HttpResponse(status=200)
