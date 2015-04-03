from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

from registers.views import idview, idListView, pdfview
from citizens.views import indexView, CitizenCreateView

#basic patterns
urlpatterns = patterns('',
    url(r'^$', indexView),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^id/(?P<idNumber>.*)$', idview),
    url(r'^pdf/(?P<idNumber>.*)$', pdfview),
    url(r'^registrate/', CitizenCreateView.as_view()),
    url(r'^attendees/$', idListView.as_view(), name='id-list'),
)

if 'grappelli' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'grappelli/', include('grappelli.urls')),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += patterns('ext_encuesta.views', (r'^registers', 'main'))
#if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL,
                          #document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
##static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)