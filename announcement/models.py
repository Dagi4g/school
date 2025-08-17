from django.db import models
from django.utils import timezone
from datetime import  timedelta

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


class Parent(models.Model):
    ''' a model for a parent in the school system. '''
    first_name = models.CharField(max_length=100,db_index=True)
    last_name = models.CharField(max_length=100,db_index=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, null=True, blank=True)
    work = models.CharField(max_length=100, null=True, blank=True)
    relationship_type = [( 'Father', 'Father'), ('Mother', 'Mother'), ('Guardian', 'Guardian')]
    relationship = models.CharField(max_length=100, null=True, blank=True, choices=relationship_type)

    def __str__(self):
        return f"{self.first_name} {self.last_name}(Email: {self.email}, Phone: {self.phone_number}, Address: {self.address}, Work: {self.work}, Relationship: {self.relationship})"

    def __repr__(self):
        return super().__repr__()

class Student(models.Model):
    ''' a model for a student in the school system. '''
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100,db_index=True)
    father_name = models.CharField(max_length=100,db_index=True)
    grand_father_name = models.CharField(max_length=100,db_index=True)
    birth_date = models.DateField(default=timezone.now()-timedelta(days=12*365))
    age = models.IntegerField(default=15)
    kebele = models.CharField(max_length=100, db_index=True)
    past_school_name = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    def __str__(self):
        return f"{self.student_name} {self.father_name} {self.grand_father_name} (Birth Date: {self.birth_date}, Age: {self.age}, Kebele: {self.kebele}, Past School: {self.past_school_name})"

    def __repr__(self):
        return super().__repr__()



class AcademicYear(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    year = models.IntegerField()
    half_semister = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.start_date and not self.half_semister:
            self.half_semister = self.start_date + timedelta(days=5*30)
            self.end_date = self.half_semister + timedelta(days=10*30)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return super().__repr__()

class Grade(models.Model):
    year_in_school_choice = {'grade 9':'fresh(9)',
                             'grade 10':'sophomore(10)',
                             'grade 11':'junior(11)',
                             'grade 12':'senior(12)'
                             }
    name = models.CharField(max_length=100,choices=year_in_school_choice.items(),default='grade 9')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name

    def __repr__(self):
        return super().__repr__()

class Section(models.Model):
    sections = [(chr(i), chr(i)) for i in range(ord('A'), ord('Z') + 1)]  # A-Z
    name = models.CharField(max_length=100, choices=sections)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f"{self.grade.name} {self.name}"

    def __repr__(self):
        return super().__repr__()