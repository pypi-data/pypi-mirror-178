from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib.auth import views as auth_views

schema_view = get_schema_view(
   openapi.Info(
      title="Movie Rent Store API",
      default_version='v1',
      description="API description"
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('rent-store/', include('rent_store.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls'), name='auth'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]