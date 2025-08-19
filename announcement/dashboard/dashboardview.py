from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import AnnouncementManagementForm
from ..models import Announcement


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementManagementForm
    template_name = 'dashboard/create_announcement.html'
    success_url = '/announcements/'

class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcement/dashboard/announcement_list.html'
    context_object_name = 'announcements'


class AnnouncementUpdateView(UpdateView):
    model = Announcement
    form_class = AnnouncementManagementForm
    template_name = 'announcement/dashboard/announcement_form.html'
    success_url = '/announcements/'

class AnnouncementDeleteView(DeleteView):
    model = Announcement
    template_name = 'announcement/dashboard/announcement_confirm_delete.html'
    success_url = '/announcements/'