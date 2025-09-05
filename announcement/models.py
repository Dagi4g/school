from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

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
    relation_ship = models.CharField(choices=relation_ship_choice)
    email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=20)
    work = models.CharField(max_length=255)
    income = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True  )
    parent_picture = models.ImageField(upload_to='parents/images', blank=True, null=True)
    class Meta:
        unique_together = ('name', 'father_name',)

    def __str__(self):
        return self.name

    def __repr__(self):
        return super().__repr__()
    

class AcademicYear(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ('start_year', 'end_year')

    def __str__(self):
        return f"{self.start_year.year}/{self.end_year.year}"

    def __repr__(self):
        return super().__repr__()

class Grade(models.Model):
    grade_choice = [('grade 9', 'Grade 9'), ('grade 10', 'Grade 10'), ('grade 11', 'Grade 11'), ('grade 12', 'Grade 12')]
    name = models.CharField(max_length=255, choices=grade_choice)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='grades')

    class Meta:
        unique_together = ('name', 'academic_year')
    def __str__(self):
        return self.name

    def __repr__(self):
        return super().__repr__()

class Section(models.Model):
    section_choice = [(chr(i), chr(i)) for i in range(65, 91)]  # A-Z
    name = models.CharField(max_length=255, choices=section_choice)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='sections')

    class Meta:
        unique_together = ('name', 'grade')

    def __str__(self):
        return f"{self.grade.name} {self.name}"

    def __repr__(self):
        return super().__repr__()

class Student(models.Model):
    student_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    grand_father_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10, choices=[('ወንድ', 'ወንድ'), ('ሰት', 'ሰት')])
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='students')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='students')
    student_picture = models.ImageField(upload_to='students/images', blank=True, null=True)

    class Meta:
        unique_together = [('student_name', 'father_name', 'grand_father_name','academic_year')]
        

    def __str__(self):
        return f"{self.student_name} {self.father_name} {self.grand_father_name}"

    def __repr__(self):
        return super().__repr__()

    
class AutoSectionGrade(models.Model):
    student_name = models.CharField(max_length=225)    
    father_name = models.CharField(max_length=225)    
    grandfather_name = models.CharField(max_length=225)
    age = models.PositiveIntegerField()
    sex_choice = [('m','M'),('f','F')]
    sex = models.CharField(max_length=10,choices=sex_choice)
    school_choice = [('junior','Junior'),('chafe','Chafe'),('tolola','Tolola'),('masho','Masho'),('lela','lela'),('betel','Betel')]
    previous_school = models.CharField(max_length=225,choices=school_choice,null=True,blank=True)
    score_choice = [(i,i) for i in range(50,101)]
    minstry_score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(100)
        ],
        choices=score_choice,
        null=True,blank=True
    )
    section  = models.CharField(max_length=20,null=True,blank=True)
    grade = models.CharField(max_length=20,choices=[('grade 9','Grade 9'),('grade 10','Grade 10'),('grade 11','Grade 11'),('grade 12','Grade 12')])
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student_name','father_name','grandfather_name'],
                name='unique_student_fullname'
            )
        ]    
    def __str__(self):
        return f'{self.student_name} {self.father_name} {self.grandfather_name}'
    
    def __rep__(self):
        return f'{self.student_name} {self.father_name} {self.grandfather_name}'
