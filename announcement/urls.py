from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'announcement'

urlpatterns = [
    path("", views.announcement_list, name="announcement_list"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   