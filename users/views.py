from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, CustomUserSignUpForm
from django.contrib.auth.decorators import login_required 
from .forms import UserUpdateForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def users_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:profile')
            else:
                messages.error(request, 'ユーザー名またはパスワードが正しくありません。')
    else:
        form = LoginForm()  # POST以外ではここでformを作成

    return render(request, 'users/login.html', {'form': form})  # どの条件でもHttpResponseを返す

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'users/profile.html', {'user':user})


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        else:
            # フォームが無効な場合もレンダリングを返す
            return render(request, 'users/profile_update.html', {'form':form})

    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html',{'form':form})

def register(request):
    return render(request, 'users/register.html')


@login_required
def home(request):
    return render(request, 'users/home.html')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('users:home')
    
@login_required
def history_view(request):
    return render(request, 'users/history.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:profile')
    else:
        form = CustomUserSignUpForm()

    return render(request, 'users/signup.html', {'form':form})