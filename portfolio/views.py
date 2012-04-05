from django.views.generic.list_detail import object_list, object_detail
from portfolio.models import *

def portfolio_list(request):
    queryset = Work.active.all()
    template_object_name = 'work'
    response = object_list(request, queryset=queryset, template_object_name=template_object_name)
    return response

def portfolio_detail(request, slug):
    queryset = Work.active.all()
    template_object_name = 'work'
    response = object_detail(request, queryset=queryset, template_object_name=template_object_name, slug=slug, slug_field='slug')
    return response