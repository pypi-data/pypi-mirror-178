from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


def manifest(request: HttpRequest) -> HttpResponse:
    return JsonResponse(dict(
        check=reverse("django_accounts_api:login_check"),
        login=reverse("django_accounts_api:login"),
        logout=reverse("django_accounts_api:logout"),
        password_change=reverse("django_accounts_api:password_change"),
    ))

def _user_details(user: DjangoUser) -> dict:
    """The details of the user to return on success"""
    return dict(
        id=user.pk,
        name=user.get_full_name(),
    )

def login_check(request) -> HttpResponse:
    """200 and details if logged in, 401 if not"""
    user: DjangoUser = request.user
    if(user.is_authenticated):
        return JsonResponse(_user_details(user))
    else:
        return HttpResponse(status=401)


class LoginPartialHTML(LoginView):
    ''' Override the Django login view to NOT redirect on successful login 
    GET - renders a partial login form
    POST - submits and validates
        if invalid returns form rendered with errors
        if valid logs the user in
    '''

    template_name = "django_accounts_api/login.html"
    def form_valid(self, form):
        """Override redirect behaviour"""
        _repressed_redirect = super().form_valid(form)
        return JsonResponse(
            _user_details(self.request.user),
            status=201
        )


class ApiLogout(LogoutView):
    ''' Override the Django logout view to NOT redirect on successful login 
    GET - actually calls POST, but will error in Django 5
    POST - logs out, returns 200
    '''

    def post(self, request, *args, **kwargs):
        _repressed_redirect_or_render = super().post(request, *args, **kwargs)
        return HttpResponse(
            status=200
        )


@method_decorator(sensitive_post_parameters(), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class ChangePasswordPartialHTML(PasswordChangeView):
    ''' Override the Django change password view to support API use
    GET - renders a partial change password form - can be accessed without auth
    '''
    template_name = "django_accounts_api/password_change.html"
    
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().post(*args, **kwargs)
        else:
            return HttpResponse(status=401)
    
    def form_valid(self, form):
        """Override redirect behaviour"""
        _repressed_redirect = super().form_valid(form)
        return JsonResponse(
            _user_details(self.request.user),
            status=201
        )