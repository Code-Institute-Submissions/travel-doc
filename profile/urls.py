from django.urls import path
from .views import regular_profile, employer_profile, profile_view, ProfileEdit


urlpatterns = [
    #path('profile/test/<int:pk>/', regular_profile, name='test_user'),
    path('profile/regular/<int:pk>/', regular_profile, name='regular_profile'),
    path('profile/employer/', employer_profile, name='employer_profile'),
    path('profile/edit/<int:pk>/', ProfileEdit.as_view(), name='profile_edit'),
    path('profile/<int:pk>/', profile_view, name='profile'),
]