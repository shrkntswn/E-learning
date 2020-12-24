from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	avatar= models.ImageField(blank=True)
	about = models.CharField(max_length=200, blank=True, null=True)
	qualification = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.user.username


class Playlist(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='playlist/images' , null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.creator.username

	def get_absolute_url(self):
		return reverse('repository:ViewVideoPlaylist', args=[self.id,])


class Video(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
	file = models.FileField(upload_to='videos/')
	description = models.CharField(max_length=200, blank=True)
	likes = models.ManyToManyField(User, related_name='likes', blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.creator.username


class Student(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	avatar = models.ImageField(blank=True)
	follow = models.ManyToManyField(Teacher, related_name='following', blank=True) 

	def __str__(self):
		return self.user.username


'''class Avatar(models.Model):
	avatar_user = models.ForeignKey(User, on_delete = models.CASCADE)
	file = models.ImageField(upload_to='profile_pics', null=True, blank=True)

	class Meta:
		verbose_name = 'avatarPhoto'
		verbose_name_plural = 'avatarPhotos'

	def __str__(self):
		return self.avatar_user.username'''


class Comment(models.Model):
	video = models.ForeignKey(Video, on_delete = models.CASCADE )
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies')
	content = models.TextField(max_length=200)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}-{}'.format(self.content[:20], str(self.user.username))

