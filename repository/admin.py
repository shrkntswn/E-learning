from django.contrib import admin
from .models import Teacher, Playlist, Video, Student, AvatarPhoto, Comment


admin.site.register(Teacher)
admin.site.register(Playlist)
admin.site.register(Video)
admin.site.register(Student)
admin.site.register(AvatarPhoto)
admin.site.register(Comment)