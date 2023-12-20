from django.urls import path
from . import views

urlpatterns = [
  
      path('login/',views.Login, name='login'),
      path('signup/',views.signup,name='signup'),
       path('logs/', views.logs_view, name='logs'),
  
]
