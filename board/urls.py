from django.urls import path
from .views import *
# from django.views.decorators.cache import cache_page

urlpatterns = [
	path('', BulletinList.as_view()),
	path('add/', BulletinCreate.as_view(), name='bulletin_create'),
	path('<int:pk>/', BulletinDetail.as_view(), name='bulletin_detail'),
	path('<int:pk>/update/', BulletinUpdate.as_view(), name='bulletin_update') ,
#	path('<int:pk>/delete/', BulletinDelete.as_view(), name='bulletin_delete'),
	path('<int:pk>/add_reply/', ReplyCreate.as_view(), name='reply_create'),
#	path('<int:pk>/edit_reply/', ReplyUpdate.as_view(), name='reply_update'),
	path('<int:pk>/delete_reply/', ReplyDelete.as_view(), name='reply_delete'),
	path('home/', Personal.as_view(), name='personal'),
	path('accept/<int:pk>', ReplyAccept.as_view(), name='reply_accept'),
]