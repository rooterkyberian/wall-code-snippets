import importlib
import io
from unittest.mock import patch

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path

with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
    importlib.import_module("this")
    ZEN = mock_stdout.getvalue()

settings.configure(DEBUG=False, ALLOWED_HOSTS="localhost", ROOT_URLCONF=__name__)
application = get_wsgi_application()
urlpatterns = [path("", lambda _: HttpResponse(ZEN, content_type="text/plain"))]

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line([__file__, "runserver", "0.0.0.0:8000"])
