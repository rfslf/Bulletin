from django.forms import ModelForm
from .models import Bulletin, Reply


class BulletinForm(ModelForm):
	class Meta:
		model = Bulletin
		fields = ['header', 'body', 'category_name']


class ReplyForm(ModelForm):
	class Meta:
		model = Reply
		fields = ['reply']