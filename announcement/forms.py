from django import forms
from .models import Announcement

class AnnouncementManagementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'image', 'video', 'audio']
