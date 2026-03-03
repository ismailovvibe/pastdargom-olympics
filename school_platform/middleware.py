from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .models import AuditLog


class RequireLoginMiddleware(MiddlewareMixin):
    """Redirect anonymous users to a registration page for most URLs.

    This middleware implements the behaviour described by the user: any
    attempt to interact with the site without a valid account should send
    the visitor to a signup page.  We exempt the homepage, authentication
    endpoints, static/media, the admin interface and API endpoints so
    basic functionality (login/register itself, password resets, etc.)
    continues working.
    """

    ALLOWED_PREFIXES = (
        '/auth/login',
        '/auth/register',
        '/auth/password_reset',
        settings.STATIC_URL,
        '/static/',
        '/media/',
        '/api/',
        '/admin/',
    )

    def process_request(self, request):
        # authenticated users are always fine
        if request.user.is_authenticated:
            return None
        path = request.path
        # allow explicit whitelist paths
        for prefix in self.ALLOWED_PREFIXES:
            if path.startswith(prefix):
                return None
        # also allow the home page
        if path in (reverse('home'), '/'):
            return None
        # otherwise redirect to registration/login page
        return redirect(settings.LOGIN_URL + f'?next={path}')


class AuditLogMiddleware(MiddlewareMixin):
    """Middleware that writes an AuditLog entry for every state-changing request.

    We record the user (if authenticated), HTTP method and path, and the
    remote IP address. This ensures the database contains a history of who
    did what, satisfying the request "hamma malumotlar bazaga saqlasin kim
    nima qilsa hammasi saqlanib ketsin".
    """

    # cache the result of table existence check to avoid repeated introspection
    _checked = False
    _exists = False

    def _check_table(self):
        if self._checked:
            return
        self._checked = True
        try:
            from django.db import connection
            self._exists = AuditLog._meta.db_table in connection.introspection.table_names()
        except Exception:
            self._exists = False

    def process_response(self, request, response):
        # Only log methods that typically mutate data
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            # if table doesn't exist we skip logging entirely
            self._check_table()
            if not self._exists:
                return response
            try:
                AuditLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    action=f"{request.method} {request.path}",
                    ip_address=request.META.get('REMOTE_ADDR'),
                )
            except Exception:
                # Guard against logging errors causing failures
                pass
        return response