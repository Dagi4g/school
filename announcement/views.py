from django.shortcuts import render
from .models import Announcement

def home(request):
    return render(request, 'announcement/home.html')

def about_us(request):
    return render(request, 'announcement/about_us.html')

def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'announcement/announcement_list.html', {'announcements': announcements})