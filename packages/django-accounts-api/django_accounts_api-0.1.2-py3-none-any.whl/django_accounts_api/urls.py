from django.urls import path
from .views import (
    ChangePasswordPartialHTML, 
    LoginPartialHTML,
    login_check,
    manifest,
    ApiLogout
)

app_name = 'django_accounts_api'
urlpatterns = [
    path('', manifest, name='manifest'),
    path('check', login_check, name='login_check'),
    path('login', LoginPartialHTML.as_view(), name='login'),
    path('logout', ApiLogout.as_view(), name='logout'),
    path('password_change', ChangePasswordPartialHTML.as_view(), name='password_change'),
]