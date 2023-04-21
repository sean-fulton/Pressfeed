from django.contrib import admin
from . import views
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import environ
import debug_toolbar

env = environ.Env()
environ.Env.read_env()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('news.urls')),
    path('', include('authentication.urls')),
    path('', include('django.contrib.auth.urls')),
]

if env('DEBUG') == 'True':
    urlpatterns += [path(r'^__debug__/', include(debug_toolbar.urls)), ]

urlpatterns += staticfiles_urlpatterns()

def startup_news_updater():
    from news.tasks import start_scheduler
    start_scheduler()
    
# startup_news_updater()
