import uuid

from django.http import HttpResponseForbidden
from django.views.defaults import permission_denied

from django_cas_ng.middleware import CASMiddleware
from django_cas_ng.views import login as cas_login, logout as cas_logout
from django.contrib.auth.views import login, logout
from django.conf import settings
# test
from django.contrib.messages import get_messages
from django.utils.translation import activate


class MoloCASMiddleware(CASMiddleware):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func == login or view_func == logout:
            return None

        if view_func == cas_login:
            return cas_login(request, *view_args, **view_kwargs)
        elif view_func == cas_logout:
            return cas_logout(request, *view_args, **view_kwargs)

        if settings.CAS_ADMIN_PREFIX:
            if not request.path.startswith(settings.CAS_ADMIN_PREFIX):
                return None
        elif not view_func.__module__.startswith('django.contrib.admin.'):
            return None

        if request.user.is_authenticated():
            if request.user.is_staff:
                return None
            else:
                return permission_denied(request, 'error')
        return super(MoloCASMiddleware, self).process_view(
            request, view_func, view_args, view_kwargs)


class Custom403Middleware(object):
    """Catches 403 responses and raises 403 which allows for custom 403.html"""
    def process_response(self, request, response):
        storage = get_messages(request)
        for message in storage:
            pass
        if isinstance(response, HttpResponseForbidden):
            return permission_denied(request, 'error')
        return response


class ForceDefaultLanguageMiddleware(object):
    """
    Ignore Accept-Language HTTP headers

    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via
    sessions or cookies

    Should be installed *before* any middleware that checks
    request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """
    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']


class AdminLocaleMiddleware(object):
    """Ensures that the admin locale doesn't change with user selection"""
    def process_request(self, request):
        if request.path.startswith('/admin/') or \
           request.path.startswith('/django-admin/'):
            activate(settings.ADMIN_LANGUAGE_CODE)


class NoScriptGASessionMiddleware(object):
    """Store a unique session key for use with GTM"""
    def process_request(self, request):
        if 'MOLO_GA_SESSION_FOR_NOSCRIPT' not in request.session:
            request.session[
                'MOLO_GA_SESSION_FOR_NOSCRIPT'] = uuid.uuid4().hex
