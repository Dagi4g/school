from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now())
    expires_at = models.DateTimeField(default=timezone.now())
    image = models.ImageField(upload_to='announcements/images', blank=True, null=True)
    video = models.FileField(upload_to='announcements/videos/', blank=True, null=True)
    audio = models.FileField(upload_to='announcements/audios/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return super().__repr__()

class ParentForm(models.Model):
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    work = models.CharField(max_length=255)
    income = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True  )

    def __str__(self):
        return self.name

    def __repr__(self):
        return super().__repr__()
