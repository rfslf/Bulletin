from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import BaseRegisterForm
from board.models import RegCode
import random
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.http import HttpResponse


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BaseRegisterForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            active = form.save(commit=False)
            active.is_active = False
            active.save()
        else:
            return HttpResponse("Ошибка!!!")
        return redirect('code', request.POST['username'])


class GetCode(CreateView):
    template_name = 'regcode.html'

    def get_context_data(self, **kwargs):
        if not RegCode.objects.filter(user=self.kwargs.get('user')).exists():
            code = random.randrange(1000, 10000)
            RegCode.objects.create(user=self.kwargs.get('user'), code=code)
            email = User.objects.get(username=self.kwargs.get('user'))
            send_mail(
                subject=f'Код активации',
                message=f'{code}',
                from_email='avdonin@unn.ru',
                recipient_list=[email.email],
            )

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = request.path.split('/')
            if RegCode.objects.filter(code=request.POST['code'], user=user[-1]).exists():
                User.objects.filter(username=user[-1]).update(is_active=True)
                RegCode.objects.filter(code=request.POST['code'], user=user[-1]).delete()
            else:
                return redirect(request.path)
        return redirect('/sign/login/')
