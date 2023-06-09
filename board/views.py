from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .filters import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BulletinForm, ReplyForm
from django.core.mail import send_mail


class BulletinList(ListView):
	model = Bulletin  # указываем модель, объекты которой мы будем выводить
	template_name = 'bulletins.html'  # указываем имя шаблона, в котором будет лежать HTML,
	# в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
	context_object_name = 'bulletins'  # это имя списка, в котором будут лежать все объекты, его надо указать,
	# чтобы обратиться к самому списку объектов через HTML-шаблон
	queryset = Bulletin.objects.order_by('-id')
	paginate_by = 10  # поставим постраничный вывод в 10 элементов


class BulletinCreate(CreateView, LoginRequiredMixin):
	model = Bulletin
	template_name = 'bulletin_add.html'
	form_class = BulletinForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = BulletinForm()
		return context

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
		if form.is_valid():
			author = form.save(commit=False)
			author.author = self.request.user
			author.save()
		return redirect('/board/home')


class BulletinDetail(DetailView, LoginRequiredMixin):
	model = Bulletin
	template_name = 'bulletin.html'
	context_object_name = 'bulletin'
	queryset = Bulletin.objects.all()

	def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
		obj = super().get_object(queryset=self.queryset)
		return obj

	def post(self, request, *args, **kwargs):
		if request.POST['reply']:
			bulletin = self.kwargs.get('pk')
			Reply.objects.create(bulletin=Bulletin.objects.get(pk=bulletin), user=self.request.user,
                				reply=request.POST['reply'], accept=False)
			id = Bulletin.objects.get(pk=self.kwargs.get('pk'))
			reply = request.POST['reply']
			email = User.objects.get(pk=id.author_id)
			post = Bulletin.objects.get(pk=self.kwargs.get('pk'))
#			send_mail(
#				subject=f'Отклики на объявление!',
#				message=f'На ваше объявление: {post}\n{self.request.user} оставил(а) отклик: {reply}',
#				from_email='snewsportal@yandex.ru',
#				recipient_list=[email.email],
#			)
		return redirect(request.path)


class BulletinUpdate(UpdateView, LoginRequiredMixin):
	template_name = 'bulletin_edit.html'
	form_class = BulletinForm

	def get_object(self, **kwargs):
		id = self.kwargs.get('pk')
		return Bulletin.objects.get(pk=id)


#class BulletinDelete(DeleteView, LoginRequiredMixin):
#	template_name = 'bulletin_delete.html'
#	queryset = Bulletin.objects.all()
#	success_url = '/board/'


class ReplyCreate(CreateView, DetailView, LoginRequiredMixin):
	template_name = 'reply_add.html'
	form_class = ReplyForm

	model = Bulletin
	context_object_name = 'bulletin'
	queryset = Bulletin.objects.all()

	def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
		obj = super().get_object(queryset=self.queryset)
		return obj

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
		if form.is_valid():
			id = self.kwargs.get('pk')
			form.bulletin = Bulletin.objects.get(pk=id)
			form.save()
		return super().get(request, *args, **kwargs)


# class ReplyUpdate(UpdateView, LoginRequiredMixin):
#	template_name = 'reply_edit.html'#
#	form_class = ReplyForm
#
#	def get_object(self, **kwargs):
#		id = self.kwargs.get('pk')
#		bulletin_to_edit = Bulletin.objects.get(pk=id)
#		return Reply.objects.get(bulletin=bulletin_to_edit)
#
		# form = self.form_class(request.POST)
		# if form.is_valid():
		# 	 id = self.kwargs.get('pk')
		# 	 form.bulletin = Bulletin.objects.get(pk=id)
		#	 form.save()
		# return super().get(request, *args, **kwargs)


class ReplyDelete(DeleteView, LoginRequiredMixin):
	template_name = 'reply_delete.html'
	queryset = Reply.objects.all()
	success_url = '/board/home/'


class Personal(ListView, LoginRequiredMixin):
	template_name = 'home.html'
	model = Reply
	context_object_name = 'home'

	def get_context_data(self, **kwargs):
		queryset = Reply.objects.filter(bulletin__author=self.request.user).order_by('-reply_time')
		context = super().get_context_data(**kwargs)
		context['filter'] = BulletinFilter(self.request.GET, queryset, request=self.request.user.pk)
		return context


class ReplyAccept(LoginRequiredMixin, TemplateView):
	template_name = 'reply_accept.html'

	def get_context_data(self, **kwargs):
		id = self.kwargs.get('pk')
		reply = Reply.objects.get(pk=id)
		email = User.objects.get(id=reply.user_id)
		# send_mail(
		# subject=f'Ваш отклик принят!',
		# message=f'Ваш отклик: {reply.text} {self.request.user} принял(а)!',
		# from_email='snewsportal@yandex.ru',
		# recipient_list=[email.email],
		# )
		print(reply)
		Reply.objects.filter(pk=id).update(accept=True)
