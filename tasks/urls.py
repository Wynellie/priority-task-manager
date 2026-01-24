from django.urls import path
from tasks import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.IndexView.as_view(),name = 'index'),
    path('<int:pk>',views.DetailedView.as_view(),name = 'detailed'),
    path('delete/<int:pk>',views.Delete.as_view(),name='delete'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name = 'tasks/auth.html'), name = 'login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register',views.RegisterView.as_view(),name='register')
]