from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from cloudinary.models import CloudinaryField


# Create your models here.



class Film(models.Model):
    film_title=models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    genre=models.CharField(max_length=100)
    summary=models.TextField(null=True)

    def get_absolute_url(self):
        return reverse('film_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.film_title

    class Meta:
        ordering=['film_title']

    def get_queryset(self):
        return Film.objects.all()


class Comment(models.Model):
    film_comment = models.ForeignKey(Film, default=1, on_delete = models.SET_DEFAULT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete = models.SET_DEFAULT)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('comment_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.content

    def __str__(self):
        return self.film_comment

    def get_queryset(self):
        return Comment.objects.all()

    class Meta:
        ordering = ('-timestamp',)


class Photo(models.Model):
    photo_film=models.ForeignKey(Film, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(blank=True, null=True)
    image_u = models.TextField(null=True,blank=True)
