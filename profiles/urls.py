from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profile_list'),
    path('<int:id>', views.profile_details, name='detail'),
    path('edit/<int:id>', views.edit_profile, name='edit'),
    path('delete/<int:id>', views.delete_profile, name='delete'),
    path('add_profile', views.add_profile, name='add_profile')
]