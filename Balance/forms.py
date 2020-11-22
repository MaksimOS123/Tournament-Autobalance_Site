from django import forms

from Balance.models import UserProfile


class SignInForm(forms.Form):
    user_name = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}))
    user_email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'psw'}), label="Password")
    password_conf = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'psw_c'}),
                                    label="Confirm password")


class TournamentForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'title'}))
    description = forms.CharField(label="Description", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'description'}), required=False)
    rules = forms.CharField(label="Fast Rules", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'Rules'}), required=False)
    full_rules = forms.CharField(label="Full Rules", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'full_rules'}), required=False)
    prizes = forms.CharField(label="Prizes", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'prizes'}), required=False)
    date = forms.DateField(label="Date", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'date'}))
    time = forms.TimeField(label="Time", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'time'}))
    schedule = forms.CharField(label="Schedule", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'schedule'}), required=False)
    contacts = forms.CharField(label="Contacts", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'contacts'}), required=False)


class UserPhoto(forms.ModelForm):
    photo = forms.ImageField(label='', required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput(attrs={'onchange': 'document.profile.submit();'}))
    class Meta:
        model = UserProfile
        fields = ('photo',)
