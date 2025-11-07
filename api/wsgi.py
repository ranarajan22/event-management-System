# api/wsgi.py -- verbose error logger for Vercel
import os
import sys
import traceback
from io import BytesIO

# ensure repo root (where manage.py is) is on sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

def log_exc(prefix=""):
    tb = traceback.format_exc()
    # print to stdout and stderr so Vercel captures it
    print(prefix + " TRACEBACK:\n" + tb)
    sys.stderr.write(prefix + " TRACEBACK:\n" + tb + "\n")

# Attempt to import Django WSGI app
try:
    # Import the Django wsgi application (adjust package name if needed)
    from final_EMS_1.wsgi import application
except Exception:
    log_exc("Error importing Django WSGI application:")
    # Re-raise so Vercel marks the function as failed and logs show the error
    raise

def handler(request, response):
    try:
        environ = request.environ.copy() if hasattr(request, "environ") else {}
        body = request.body or b""
        environ["wsgi.input"] = BytesIO(body)
        environ["CONTENT_LENGTH"] = str(len(body))
        environ["REQUEST_METHOD"] = request.method
        environ["PATH_INFO"] = request.path
        environ["QUERY_STRING"] = (
            request.query_string.decode() if isinstance(request.query_string, (bytes, bytearray)) else (request.query_string or "")
        )

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
    except Exception:
        log_exc("Error during request handling:")
        # re-raise to make failure visible in logs and to return 500
        raise
