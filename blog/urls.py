from django.conf.urls import url
from . import views
from . import forms


urlpatterns = [
	url(r'^$', views.index, name = 'index' ),
	url(r'^post/(?P<pk>\d+)/$', views.PostPage.as_view(), name = 'post' ),
	url(r'^post/(?P<action>\w+)/(?:(?P<pk>\d+)/)?$', views.PostHandler.as_view(), name = 'post_handler'),
	url(r'^cathegory/(?P<cathegory>\w+)/$', views.cathegory, name = 'cathegory'),
	url(r'^author/(?P<author>\w+)/$', views.author, name = 'author'),
	url(r'^user/profile/$', views.profile, name = 'profile'),
	url(r'^user/login/$', views.user_login, name = 'user_login'),
	url(r'^user/logout/$', views.user_logout, name = 'user_logout'),
	url(r'^user/register/$', views.UserRegister.as_view(), name = 'user_register'),
	url(r'^user/update/$', views.UserUpdate.as_view(), name = 'user_update'),
	url(r'^user/password-change/$', views.password_change, name = 'password_change'),
	url(r'^comment/(?P<action>\w+)/(?P<pk>\d+)/$', views.CommentHandler.as_view(), name = 'comment_handler'),
	url(r'^is-auth/$', views.is_auth, name = 'is_auth'),
	url(r'^statistics/(?P<pk>\d+)/$', views.statistics, name = 'statistics'),
]
