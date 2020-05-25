from django.conf.urls import url 
from names import views 
 
urlpatterns = [ 
    url(r'^$', views.name_list),
    url(r'^(?P<pk>[0-9]+)$', views.name_detail),
    url(r'^viewnames$', views.view_name_list),
    url(r'^meaningname$', views.meaning_name)
]
