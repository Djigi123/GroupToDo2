from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Добавь этот импорт
from tasks import views as task_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('signup/', task_views.signup, name='signup'),

    # Добавь эту строку, чтобы путь /login/ заработал:
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('accounts/', include('django.contrib.auth.urls')),
]