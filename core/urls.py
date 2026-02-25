from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from notes.views import NoteViewSet
from rest_framework.authtoken import views as auth_views
from users.views import CustomLoginView, LogoutView, ProfileViewSet, RegisterView

router = DefaultRouter()

router.register(r'notes', NoteViewSet, basename='notes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', CustomLoginView.as_view(), name='login'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/user/', ProfileViewSet.as_view(), name='profile'),
    path('api/auth/', include('rest_framework.urls')),
]
