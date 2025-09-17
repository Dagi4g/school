# Copyright 2025 Dagim Genene
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


from ..models import Announcement
from ..forms import AnnouncementManagementForm


class DashboardAnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/announcements/show_announcement.html'
    context_object_name = 'announcements'

class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementManagementForm
    template_name = 'dashboard/announcements/create_announcement.html'
    success_url = '/show_announcement/'
    
    
class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'dashboard/announcements/announcement_detail.html'
    context_object_name = 'announcement'


class AnnouncementUpdateView(LoginRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementManagementForm
    template_name = 'dashboard/announcements/update_announcement.html'
    success_url = '/show_announcement/'

class AnnouncementDeleteView(LoginRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'dashboard/announcements/confirm_announcement_deletion.html'
    success_url = '/show_announcement/'
