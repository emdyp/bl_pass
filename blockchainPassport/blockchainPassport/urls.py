from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from registers.views import idview

#basic patterns
urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^id/(?P<idNumber>.*)$', idview)
                       )
if 'grappelli' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'grappelli/', include('grappelli.urls')),)
#urlpatterns += patterns('ext_encuesta.views', (r'^registers', 'main'))
#if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL,
                          #document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
##static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)