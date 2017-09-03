from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings as s
from apps.home.views import index

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^redactor/', include('redactor.urls')),
                       url(r'^blog/', include('blog.urls')),
                       url(r'^account/', include('account.urls')),
                       url(r'^$', view=index, name='home'),
)

# static files serving in development
if s.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
