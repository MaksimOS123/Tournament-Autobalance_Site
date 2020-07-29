from django import forms

from Balance.models import UserProfile


class SignInForm(forms.Form):
    user_name = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}))
    user_first_name = forms.CharField(label="First name", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name'}))
    user_last_name = forms.CharField(label="Last name", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name'}))
    user_email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'psw'}), label="Пароль")
    password_conf = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'psw_c'}),
                                    label="Подтвердите пароль")


class TournamentForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'title'}))
    description = forms.CharField(label="Description", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'description'}))
    rules = forms.CharField(label="Fast Rules", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'Rules'}))
    full_rules = forms.CharField(label="Full Rules", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'full_rules'}))
    prizes = forms.CharField(label="Prizes", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'prizes'}))
    date = forms.DateField(label="Date", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'date'}))
    time = forms.TimeField(label="Time", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'time'}))
    schedule = forms.CharField(label="Schedule", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'schedule'}))
    contacts = forms.CharField(label="Contacts", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'contacts'}))


class UserPhoto(forms.ModelForm):
    photo = forms.ImageField(label='', required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('photo',)
