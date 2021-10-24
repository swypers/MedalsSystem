from django import forms
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):# Метод,который сразу проверит наличие юзера и соответ пароля
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Такой пользователь отсутствует')
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', )

    def clean_password2(self, *args, **kwargs):# Метод,который сразу проверит наличие юзера и соответ пароля
        data = self.cleaned_data

        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
            user = authenticate(username=username, password=password)
        else:
            return data['password2']
