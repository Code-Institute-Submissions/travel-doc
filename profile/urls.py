from django.urls import path
from .views import *


urlpatterns = [
    path('accounts/signup/',
        CustomSignupView.as_view(), name='account_signup'),
    path('profile/regular/<int:pk>/', regular_profile, name='regular_profile'),
    path('profile/employer/<int:pk>/',
        employer_profile, name='employer_profile'),
    path('profile/edit/<int:pk>/', ProfileEdit.as_view(), name='profile_edit'),
    path('profile/<int:pk>/', profile_view, name='profile'),
]
