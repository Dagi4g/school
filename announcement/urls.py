from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .dashboard import dashboardview
from . import views

app_name = 'chencha'

urlpatterns = [
    path("", views.home, name="home"),
    path("announcements/", views.announcement_list, name="announcement_list"),
    path("about_us/", views.about_us, name="about_us"),
    # the school dashboard.
    path("create_announcement/", dashboardview.AnnouncementCreateView.as_view(), name="create_dashboard"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   