# user urls
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register/", views.register, name="register"),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.edit_profile, name='profile-edit'),
] 


