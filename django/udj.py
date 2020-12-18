from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpRequest, HttpResponse
from django.urls import re_path

settings.configure(DEBUG=False, ALLOWED_HOSTS="localhost", ROOT_URLCONF=__name__)
application = get_wsgi_application()


def hello(request: HttpRequest, name: str = "") -> HttpResponse:
    name = name or request.META.get("REMOTE_ADDR")
    return HttpResponse(f"Hello {name}!")


urlpatterns = (re_path(r"^(?P<name>\w*)$", hello),)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line([__file__, "runserver"])
