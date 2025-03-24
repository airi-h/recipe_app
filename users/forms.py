from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User =get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['user_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'border rounded-lg px-4 py-2 w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border rounded-lg px-4 py-2 w-full'}),
            'password1': forms.PasswordInput(attrs={'class': 'border rounded-lg px-4 py-2 w-full'}),
            'password2': forms.PasswordInput(attrs={'class': 'border rounded-lg px-4 py-2 w-full'}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # passward1 の規定のヘルプテキストを削除
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード (確認)'


class LoginForm(forms.Form):
    user_name = forms.CharField(label='ユーザー名')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'email']

class CustomUserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['user_name', 'email','password1', 'password2']
