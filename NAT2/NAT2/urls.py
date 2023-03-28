from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.urls import path, include
from App import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('logout/', views.logout),
    path('UserData/', views.show_user_data),

]
