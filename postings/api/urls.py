
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', BlogPostRUDView.as_view(), name="post_rud" ),
    url(r'^$', BlogPostAPIView.as_view(), name="post_create" ),

]