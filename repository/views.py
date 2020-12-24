from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher, Student, Playlist, Video
from .forms import UserLoginForm, UserRegistrationForm, PlaylistForm, VideoCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime
from django.http import HttpResponseRedirect, JsonResponse, Http404



# FOR TEACHERS REGISTRATION
def registration(request):
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			password = form.cleaned_data['password1']
			user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
			user.save()
			if request.POST.get('exampleRadios') == 'teacher':
				Teacher.objects.create(user = user,)
			else:
				Student.objects.create(user = user,)
			login(request, user)
			return redirect('repository:home')
	else:
		form=UserRegistrationForm()
	return render(request, 'accounts/registration.html', {'form':form})


# FOR LOGIN
def userLogin(request):
	if request.method == 'POST':
		form =UserLoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				if request.POST.get('rememberMeCheck', None) == None:
					request.session.set_expiry(0)
				return redirect('repository:home')
			else:
				message = "Either user does not exists or password not correct. Please try again."
				context = {'form': form, 'message':message}
				return render(request, 'accounts/login.html', context)
	else:
		form = UserLoginForm()
		context = {'form': form}
		return render(request, 'accounts/login.html', context)

# FOR LOGOUT
def userLogout(request):
	logout(request)
	request.session.clear_expired()
	return redirect('repository:login')



def home(request):
	teacher = Teacher.objects.filter(user=request.user)
	#playlists = Playlist.objects.all()
	form = PlaylistForm()
	if request.user == teacher[0].user:
		playlists = Playlist.objects.filter(creator=request.user)

	context = {'playlists':playlists, 'form':form}
	return render(request, 'home.html', context)


def createPlaylist(request):
	if request.method == 'POST':
		form = PlaylistForm(data = request.POST, files=request.FILES)
		if form.is_valid():
			playlist = form.save(commit=False)
			playlist.creator = request.user
			playlist.created=datetime.now()
			playlist.save()
	return redirect('repository:home')


def ViewVideoPlaylist(request, id):
	form = VideoCreationForm()
	playlist = get_object_or_404(Playlist, id=id)
	videos = Video.objects.filter(playlist__id = playlist.id)
	context={'playlist':playlist, 'videos':videos, 'form':form}
	return render(request, 'playlist.html', context)


def CreateVideoPlaylist(request, id):
	playlist = get_object_or_404(Playlist, id=id)
	if request.method == 'POST':
		form = VideoCreationForm(data = request.POST, files=request.FILES)
		if form.is_valid():
			video = form.save(commit=False)
			video.playlist = playlist
			video.creator = request.user
			video.created=datetime.now()
			video.save()
	return HttpResponseRedirect(playlist.get_absolute_url())







