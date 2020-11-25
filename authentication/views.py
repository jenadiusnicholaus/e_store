from django.contrib import messages
from django.shortcuts import render, redirect
from authentication.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from authentication.forms import UserSignUpForm, SinInForm
# Create your views here.
from django.views.generic.base import View


class UserSignUp(View):
    def get(self, *args, **kwargs):

        context = {}
        form = UserSignUpForm(self.request.POST or None)
        context['form'] = form
        return render(self.request, 'authentication/register.html', context)

    def post(self, request, *args, **kwargs):
        form = UserSignUpForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('repeat_password')
            mobile = form.cleaned_data.get('mobile')
            tin = form.cleaned_data.get('tin')

            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                # if password == password2:
                User.objects.create_user(email, password, mobile=mobile, tin=tin, username=username, is_active=False)
                # it going to be userd later in the email sending
                user = User.objects.get(username=username, email=email)
                # TODO send email address to activate a user if you want it to
                messages.warning(self.request, f'Login now')
                return redirect('sign_in')
            else:
                messages.warning(self.request, 'Looks like a username with that email or password already exists')
                return redirect("sign_up")
        else:
            print('from not valid')
            messages.warning(self.request, 'Form not valid')
        return redirect('sign_up')


class UserSignIn(View):
    def get(self, request, *args, **kwargs):
        form = SinInForm()
        context = {
            'form': form
        }
        return render(request, template_name='authentication/signin.html', context=context)

    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')
            user_auth = authenticate(email=email, password=password)

            if user_auth:
                # we need to check if the auth_user is activate to our system
                if user_auth.is_active:
                    # if not request.POST.get('remember_me', None):
                    # make the session to end in one mouth
                    login(request, user_auth)
                    messages.info(self.request, 'welcome home ')
                    return redirect('/')

                else:
                    messages.info(self.request, 'Your account was inactive.Try to activate your account now')
                    return redirect('sign_in')
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(email, password))
                messages.warning(self.request, 'Invalid login details given,')
                return redirect("sign_in")


def user_sign_out(request, ):
    # Log out the user.
    logout(request)
    # Return to homepage.
    messages.warning(request, 'Your signed Out, Login again')
    return redirect('sign_in')
