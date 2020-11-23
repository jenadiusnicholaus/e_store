from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.views.generic.base import View


class signIn(View):
    def get(self):
        pass

    def post(self):
        pass


class signUp(View):
    def get(self, *args, **kwargs):
        context = {}
        form = UserCreationForm(self.request.POST or None)
        context['form'] = form
        return render(self.request, 'authentication/register.html', context)

    def post(self, *args, **kwargs):
        form = UserCreationForm(self.request.POST or None)
        if form.is_valid():
            user = form.save()
            login(self.request, user)
            messages.success(self.request, 'welcome back')
            return redirect('/')
        messages.success(self.request, 'form is not valid')
        return redirect('sign_up')


def user_sign_out(request, ):
    # Log out the user.
    logout(request)
    # Return to homepage.
    messages.warning(request, 'Your signed Out, Login again')
    return redirect('/login/')
