from django.shortcuts import render
from django.views.generic import ListView

from .models import Announcement

def home(request):
    return render(request, 'announcement/home.html')

def about_us(request):
    return render(request, 'announcement/about_us.html')

class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcement/announcement_list.html'
    context_object_name = 'announcements'