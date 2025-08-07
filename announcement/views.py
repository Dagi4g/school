from django.shortcuts import render
from .models import Announcement

def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'announcement/announcement_list.html', {'announcements': announcements})