from django.urls import path
from .views import register_participant,success_page,add_car,home,signup

urlpatterns = [
    path('register/', register_participant, name='register'),
     path('success/', success_page, name='success_page'),
      path('add_car/<int:participant_id>/', add_car, name='add_car'),
      path('', home, name='home'),
      path('signup/',signup,name='signup'),
  
]
