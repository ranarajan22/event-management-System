# api/wsgi.py
import os
import sys
from io import BytesIO
from django.core.wsgi import get_wsgi_application

# ensure project root (repo root where manage.py lives) is on PYTHONPATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# point to your settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_EMS_1.settings")

# create WSGI app
application = get_wsgi_application()

def handler(request, response):
    environ = request.environ.copy() if hasattr(request, "environ") else {}
    body = request.body or b""
    environ["wsgi.input"] = BytesIO(body)
    environ["CONTENT_LENGTH"] = str(len(body))
    environ["REQUEST_METHOD"] = request.method
    environ["PATH_INFO"] = request.path
    environ["QUERY_STRING"] = (
        request.query_string.decode()
        if isinstance(request.query_string, (bytes, bytearray))
        else (request.query_string or "")
    )

    # required WSGI defaults
    environ.setdefault("SERVER_NAME", "vercel")
    environ.setdefault("SERVER_PORT", "80")
    environ.setdefault("wsgi.version", (1, 0))
    environ.setdefault("wsgi.url_scheme", "https")
    environ.setdefault("wsgi.errors", sys.stderr)
    environ.setdefault("wsgi.multithread", True)
    environ.setdefault("wsgi.multiprocess", False)
    environ.setdefault("wsgi.run_once", False)

    body_parts = []
    status_headers = {}

    def start_response(status, headers, exc_info=None):
        status_headers["status"] = status
        status_headers["headers"] = headers

    result = application(environ, start_response)

    for part in result:
        body_parts.append(part)
    if hasattr(result, "close"):
        result.close()

    response.status = int(status_headers.get("status", "200 OK").split()[0])
    for k, v in status_headers.get("headers", []):
        response.set_header(k, v)
    response.write(b"".join(body_parts))
    return response
