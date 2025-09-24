from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password/change/',
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html'
         ),
         name='password_change'),
    path('password/change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'
         ),
         name='password_change_done'),

    # URLs d'authentifcation :
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),

]
