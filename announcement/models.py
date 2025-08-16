from django.db import models

class Announcement(models.Model):
    """
    a model for an announcement in the system.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='announcements/images', blank=True, null=True)
    video = models.FileField(upload_to='announcements/videos/', blank=True, null=True)
    audio = models.FileField(upload_to='announcements/audios/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return super().__repr__()

class Student(models.Model):
    ''' a model for a student in the school system. '''
    first_name = models.CharField(max_length=100,db_index=True)
    last_name = models.CharField(max_length=100,db_index=True)
    grade = models.IntegerField(db_index=True)
    letters = [(chr(i), chr(i)) for i in range(ord('A'), ord('Z') + 1)]  # A-Z
    section = models.CharField(max_length=10, choices=letters)

    def __str__(self):
        return f"{self.first_name} {self.last_name}(Grade: {self.grade}, Section: {self.section})"

    def __repr__(self):
        return super().__repr__()