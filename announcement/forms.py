from django import forms
from django.forms import inlineformset_factory
from .models import (Announcement,Student,Parent,Section,Grade,AcademicYear)

class AnnouncementManagementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'image', 'video', 'audio', 'created_at','expires_at']
        labels = {
            'title': 'ሪዕስ',
            'content': 'ዝረዝር ሐተታ',
            'image': 'ምስል',
            'video': 'ቪዲዮ',
            'audio': 'ድምፅ',
            'created_at' :  'የተለጠፈበት ቀን',
            'expires_at' : 'እስክ'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'audio': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'created_at': forms.DateInput(attrs={'type':'date'}),
            'expires_at': forms.DateInput(attrs={'type':'date'}),
        }
        

class StudentManagementForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ['student_name', 'father_name', 'grand_father_name','birth_date', 'age', 'sex', 'email', 'phone',]
        labels = {
            'student_name': 'የተማሪ ስም',
            'father_name': 'የአባት ስም',
            'grand_father_name': 'የአያት ስም',
            'birth_date': 'የልደት ቀን',
            'age': 'እድሜ',
            'sex': 'ፆታ',
            'email': 'ኢሜይል',
            'phone': 'ስልክ',
        }
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'grand_father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type':'date', 'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}, choices=[('male', 'ወንድ'), ('female', 'ሴት'), ('other', 'ሌላ')]),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self,*args,**kwargs):
        section = kwargs.pop('section',None)
        super().__init__(*args,**kwargs)
        if section:
            self.fields['section'].initial = section
            self.fields['section'].wedgets = form.HiddenInput()
            
    

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['name','father_name','relation_ship','email','phone','work','income']
        

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name']
        
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name']
        
class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['start_year','end_year']
        widgets = {
            'start_year': forms.DateInput(attrs={'type':'date'}),
            'end_year' : forms.DateInput(attrs={'type':'date'}),
        }



