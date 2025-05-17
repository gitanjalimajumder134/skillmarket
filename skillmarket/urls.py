from django.urls import path

from .views import BookSkillClass, ChatMessagesView, MyBookingsView, SkillClassListCreate, UserProfileView, health_check
from .views_auth import LoginUser, RegisterUser
urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('auth/register/', RegisterUser.as_view(), name='register'),
    path('auth/login/', LoginUser.as_view(), name='login'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('skills/', SkillClassListCreate.as_view(), name='skills-list-create'),  # GET + POST
    path('bookings/', BookSkillClass.as_view(), name='book-skill-class'),        # POST
    path('bookings/my/', MyBookingsView.as_view(), name='my-bookings'),          # GET
    path('messages/', ChatMessagesView.as_view(), name='chat-messages'),
]