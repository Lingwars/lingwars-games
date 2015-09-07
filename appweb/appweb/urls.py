
from django.conf.urls import include, url
from django.contrib import admin

from .views import login, logout, home, register


admin.site.site_header = 'Lingwargs | Games'
admin.site.index_title = 'Lingwargs | Games'


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', home, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register, name='register'),

    url(r'^', include('engine.urls')),

    url(r'^word2def/', include('games.word2def.urls', namespace='word2def')), # TODO: Auto-add because we need namespace to be that 'id',

]
