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
    path ("dashboard/", dashboardview.DashBoard.as_view(), name="dashboard"),
    path("create_announcement/", dashboardview.AnnouncementCreateView.as_view(), name="create_announcement"),
    path("show_announcement/", dashboardview.AnnouncementListView.as_view(), name="show_announcement"),
    path("update_announcement/<int:pk>/", dashboardview.AnnouncementUpdateView.as_view(), name="update_announcement"),
    path("announcement_detail/<int:pk>/", dashboardview.AnnouncementDetailView.as_view(), name="announcement_detail"),
    path("delete_announcement/<int:pk>/", dashboardview.AnnouncementDeleteView.as_view(), name="delete_announcement")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   