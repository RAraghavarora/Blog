from django.conf.urls import url,include
from . import views

app_name='blog'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^view/(?P<slug>[-\w]+)/$',views.view_post, name='view_post'),
	url(r'^category/(?P<slug>[-\w]+)/$',views.view_category, name='view_category'),
	url(r'^new$',views.post_new, name='post_new'),
	#url(r'accounts/', include('registration.backends.hmac.urls')),
	url(r'^post/(?P<slug>[-\w]+)$', views.post_edit, name='post_edit'),
	url(r'logout/$', views.logout_page,name='logout_page'),
	url(r'register/$',views.register_page,name='register_page'),
	url(r'search/$', views.search, name='search'),
	url(r'^follow/(?P<pk>[0-9]+)', views.follow,name='follow'),
	#url(r'login/$', views.login_page, name='login_page'),
	]
#[^\.]       ?????
#study regular expressions again!
