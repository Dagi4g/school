from django.views.generic import CreateView,ListView,DeleteView,UpdateView,DetailView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import AnnouncementManagementForm
from ..models import (Announcement,Student,Parent,AcademicYear,Grade,Section)

class DashBoard(LoginRequiredMixin, TemplateView):
    model = Announcement
    template_name = 'dashboard/home.html'
    

'''announcement management view'''

class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementManagementForm
    template_name = 'dashboard/create_announcement.html'
    success_url = '/show_announcement/'

class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/show_announcement.html'
    context_object_name = 'announcements'

class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'dashboard/announcement_detail.html'
    context_object_name = 'announcement'


class AnnouncementUpdateView(LoginRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementManagementForm
    template_name = 'dashboard/update_announcement.html'
    success_url = '/show_announcement/'

class AnnouncementDeleteView(LoginRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'dashboard/confirm_announcement_deletion.html'
    success_url = '/show_announcement/'

'''student management view'''

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'dashboard/student/show_students.html'
    context_object_name = 'students'
