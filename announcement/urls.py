from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'chencha'

urlpatterns = [
    path("", views.home, name="home"),
    path("announcements/", views.announcement_list, name="announcement_list"),
    path("about_us/", views.about_us, name="about_us"),
    path("student_section_lookup/", views.student_section_lookup, name="student_section_lookup"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   