from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, signup_view

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  # 'user_login' 関数名も一致しているか？
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('home/', views.home, name='home'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('history/', views.history_view, name='history'),
    path('signup/', signup_view, name='signup'),
    path('register/', views.register, name='register'),
]
