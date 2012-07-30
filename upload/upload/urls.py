from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'image.views.uploadimage'),
    url(r'^del/(?P<image_id>[0-9]+)/$', 'image.views.delimage'),
    # url(r'^upload/', include('upload.foo.urls')),

)
