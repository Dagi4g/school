from django.db import models
from django.utils import timezone
from datetime import timedelta

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

class Parent(models.Model):
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    relation_ship_choice = [('አባት', 'አባት'), ('እናት', 'እናት'), ('አሳዳጊ', 'አሳዳጊ'), ('ሌላ', 'ሌላ')]
    relation_ship = models.CharField(max_length=255, choices=relation_ship_choice)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    work = models.CharField(max_length=255)
    income = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True  )

    def __str__(self):
        return self.name

    def __repr__(self):
        return super().__repr__()
    

class AcademicYear(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"

    def __repr__(self):
        return super().__repr__()

class Grade(models.Model):
    grade_choice = [('grade 9', 'Grade 9'), ('grade 10', 'Grade 10'), ('grade 11', 'Grade 11'), ('grade 12', 'Grade 12')]
    name = models.CharField(max_length=255, choices=grade_choice)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __repr__(self):
        return super().__repr__()

class Section(models.Model):
    section_choice = [(chr(i), chr(i)) for i in range(65, 91)]  # A-Z
    name = models.CharField(max_length=255, choices=section_choice)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return self.name

    def __repr__(self):
        return super().__repr__()

class Student(models.Model):
    student_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    grand_father_name = models.CharField(max_length=255)
    birth_date = models.DateField(default=timezone.now()-timedelta(days=365*15))
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.student_name} {self.father_name} {self.grand_father_name}"

    def __repr__(self):
        return super().__repr__()