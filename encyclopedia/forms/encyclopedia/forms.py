from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Search(forms.Form):
  query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia', 'class': 'search'} ), label="")

class CreatePage(forms.Form):
  title = forms.CharField(label='Name of Page:', widget=forms.TextInput(attrs={'class': 'form-control w-75 p-3'}))
  content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-75 p-3'}), label="Title and Content of Page")
  
class EditingForm(forms.Form):
  entry = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control p-5 w-75'}), label="Editing Page:", required=False )
  
class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control w-75'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control w-75'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control w-75'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control w-75'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control w-75'}))
  password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control w-75'}))