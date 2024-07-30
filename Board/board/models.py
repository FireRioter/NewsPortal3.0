from django.contrib.auth.models import AbstractUser
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('Top hardspots', 'Лучшие тяжелые споты'),
        ('Top ezespots', 'Лучшие легкие споты'),
        ('TierListPveClasses', 'Лучшие пве классы'),
        ('TierListPvpClasses', 'Лучшие пвп классы'),
        ('TopProfession', 'Лучшая профессия'),
    ]

    title = models.CharField(max_length=255)
    content = CKEditor5Field('Контент')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title

class Response(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default = False)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Response by {self.user.username} on {self.ad.title}"

class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(CustomUser)