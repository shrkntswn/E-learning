from django import forms
from .models import Teacher, Playlist, Video, Student, Comment
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
	username= forms.CharField(label="Username",max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label="Password", max_length=100, min_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(UserCreationForm):
	first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control', 'placeholder':'Fist Name'}))
	last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control','placeholder':'Last Name'}))
	username = forms.CharField(label="Username",max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'}))
	password1 = forms.CharField(label="Password", max_length=100, min_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))
	password2 = forms.CharField(label="Confirm Password", max_length=100, min_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirm Password'}))

	def clean_username(self):
		username = self.cleaned_data['username']
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise ValidationError('Username is already taken.')
		else:
			return username		
		
	def clean(self):
		cleaned_data = super().clean()
		p1 = cleaned_data.get('password1')
		p2 = cleaned_data.get('password2')
		if p1 and p2:
			if p1 != p2:
				raise ValidationError('Passwords do not match')


class UserEditForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','readonly':'readonly'}))
	first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
	class Meta:
		model = User
		fields = {
			'username', 'first_name', 'last_name',
		}


class TeacherCreationForm(forms.Form):
	about = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control','placeholder':'About'}))
	qualifications = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control','placeholder':'Qualifications'}))
	class Meta:
		model = User


class StudentCreationForm(forms.Form):
	class Meta:
		model = User


class UserCommentForm(forms.ModelForm):
	content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control border border-info', 'rows':1,}))

	class Meta:
		model = Comment
		fields = {'content',}


class PlaylistForm(forms.ModelForm):
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control','placeholder':'Title'}))
	description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Description', 'rows':2}))
	class Meta:
		model = Playlist
		fields = {'title', 'description', 'image'}
	field_order = ['title', 'description', 'image']
	

class VideoCreationForm(forms.ModelForm):
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control','placeholder':'Title'}))
	description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Description', 'rows':2}))
	class Meta:
		model = Video
		fields = {'title', 'description', 'file'}
	field_order = ['title', 'description', 'file']