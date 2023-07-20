from django.contrib import admin
from django.urls import path, include
from watcha.views import base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('netplix/', include('watcha.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'),
]
