from django import forms
from .models import Announcement

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
        
    
        
