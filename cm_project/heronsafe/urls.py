from django.urls import path
from . import views

urlpatterns = [
   path('', views.base, name="base"),
   path('dashboard', views.home, name="home"),
   path('student/<str:pk_test>/', views.student, name="student"),
   path('assessment/<str:pk_test>/', views.assessment, name="assessment"),
   path('register', views.registerPage, name="register"),
   path('login', views.loginPage, name="login"),
   path('logout/', views.logoutUser, name="logout"),
]