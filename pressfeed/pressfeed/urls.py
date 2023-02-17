from django.contrib import admin
from django.urls import path, include
import environ
import debug_toolbar

env = environ.Env()
environ.Env.read_env()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('', include('authentication.urls')),
]

if env('DEBUG') == 'True':
    urlpatterns += [path(r'^__debug__/', include(debug_toolbar.urls)),]