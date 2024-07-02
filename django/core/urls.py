from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import include, path

from network.forms import UserLoginForm
from network.views import SignUpView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('network.urls')),
    path('login/', LoginView.as_view(form_class=UserLoginForm,
                                     template_name='network/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", SignUpView.as_view(), name="register"),


]
