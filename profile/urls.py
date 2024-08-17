from django.urls import path
from .views import regular_profile, employer_profile, profile_view, ProfileEdit


urlpatterns = [
    path('profile/<int:pk>/', regular_profile, name='regular_profile'),
    path('employer/', employer_profile, name='employer_profile'),
    path('profile/edit/<int:pk>/', ProfileEdit.as_view(), name='profile_edit'),
    path('profile/', profile_view, name='profile'),
]