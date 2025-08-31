from django.shortcuts import render
from django.views.generic import ListView,CreateView

from .forms import AutoSectionGradeForm
from .models import Announcement,AutoSectionGrade

def home(request):
    return render(request, 'announcement/home.html')

def about_us(request):
    
    return render(request, 'announcement/about_us.html')

class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcement/announcement_list.html'
    context_object_name = 'announcements'

class AutoGradeSectionCreateView(CreateView):
    model = AutoSectionGrade
    form_class = AutoSectionGradeForm
    template_name ='autograde/add_student.html'
    success_url = 'autograde'
    