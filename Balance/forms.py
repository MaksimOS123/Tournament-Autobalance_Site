from django import forms

class SignInForm(forms.Form):
    user_name = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}))
    user_first_name = forms.CharField(label="First name", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name'}))
    user_last_name = forms.CharField(label="Last name", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name'}))
    user_email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'psw'}), label="Пароль")
    password_conf = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'psw_c'}),
                                    label="Подтвердите пароль")
