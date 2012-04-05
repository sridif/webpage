from django.conf.urls.defaults import *

urlpatterns = patterns('portfolio.views',
    url(r'^$', view='portfolio_list', name='portfolio_work_list'),
    url(r'^(?P<slug>[-\w]+)/$', view='portfolio_detail', name='portfolio_work_detail'),
)