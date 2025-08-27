from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

from .models import (Announcement,Student,Parent,Section,Grade,AcademicYear)


class AnnouncementManagementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'image', 'video', 'audio', 'created_at','expires_at',]
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
        fields = ['student_name', 'father_name', 'grand_father_name','birth_date', 'age', 'sex', 'email', 'phone','student_picture']
        labels = {
            'student_name': 'የተማሪ ስም',
            'father_name': 'የአባት ስም',
            'grand_father_name': 'የአያት ስም',
            'birth_date': 'የልደት ቀን',
            'age': 'እድሜ',
            'sex': 'ፆታ',
            'email': 'ኢሜይል',
            'phone': 'ስልክ',
            'student_picture': 'የተማሪ ምስል'
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
        
        def validate_unique(self):
            try:
                super().validate_unique()
            except ValidationError:
                raise ValidationError("A student with this name and father's name already exists in this academic year.")

    def __init__(self,*args,**kwargs):
        section = kwargs.pop('section',None)
        super().__init__(*args,**kwargs)
        if section:
            self.fields['section'].initial = section
            self.fields['section'].wedgets = form.HiddenInput()
            
    


class ParentForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="ስም",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'የአሳዳግ ስም'})
    )
    
    father_name = forms.CharField(
        max_length=255,
        label="የአባት ሥም",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'የአባት ስም'})
    )
    
    relation_ship = forms.ChoiceField(
        choices=Parent.relation_ship_choice,
        label="ዝምድና",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        label="እማኢል",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'እምይል'})
    )
    phone = forms.CharField(
        required=False,
        label="ስልክ",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ስልክ'})
    )
    work = forms.CharField(
        required=False,
        label="ስራ",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ስራ'})
    )
    income = forms.DecimalField(
        required=False,
        label="ደሞዝ",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'የወር ደሞዝ'})
    )
    parent_picture = forms.ImageField(
        required=True,
        label="የወላጅ ምስል",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )



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


class StudentLookUpForm(forms.Form):
    name = forms.CharField(max_length=100,label='የተማር ስም')
    father_name = forms.CharField(max_length=100, label='የአባት ስም')
    grand_father_name  = forms.CharField(max_length=100, label='የአያት ስም')
    grade = forms.ChoiceField(
        choices=Grade.grade_choice,
        label='ክፍል',
        )