from django.conf.urls import url
from django.urls import path
from names import views 
 
urlpatterns = [ 
    url(r'^$', views.name_list),
    url(r'^(?P<pk>[0-9]+)$', views.name_detail),
    url(r'^viewnames$', views.view_name_list),
    url(r'^viewnames2$', views.view_name_list_2),
    url(r'^meaningname$', views.meaning_name),
    url(r'^top$', views.top_like),
    path('like/<int:pk>', views.like_name),
    path('register/', views.create_user),
    path('login/', views.login_user),
    path('test/', views.test)
]
