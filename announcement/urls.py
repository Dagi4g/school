from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .dashboard import dashboardview
from . import views

app_name = 'chencha'

urlpatterns = [
    path("", views.home, name="home"),
    
    path("announcements/", views.AnnouncementListView.as_view(), name="announcement_list"),
    path("about_us/", views.about_us, name="about_us"),
    # the school dashboard.
    path ("dashboard/", dashboardview.DashBoard.as_view(), name="dashboard"),
    path("create_announcement/", dashboardview.AnnouncementCreateView.as_view(), name="create_announcement"),
    path("show_announcement/", dashboardview.DashboardAnnouncementListView.as_view(template_name='dashboard/announcements/show_announcement.html'), name="show_announcement"),
    path("update_announcement/<int:pk>/", dashboardview.AnnouncementUpdateView.as_view(), name="update_announcement"),
    path("announcement_detail/<int:pk>/", dashboardview.AnnouncementDetailView.as_view(), name="announcement_detail"),
    path("delete_announcement/<int:pk>/", dashboardview.AnnouncementDeleteView.as_view(), name="delete_announcement"),
    # student related dashboard view
    path("students/", dashboardview.GeneralStudentListView.as_view(), name="student_list"),
    path("academic_year/<int:ay_pk>/grade/<int:grade_pk>/section/<int:section_pk>/register_student/",dashboardview.StudentCreateView.as_view(),name="register_student"),
    # section related views
    path("create_section/<int:grade_pk>/<int:ay_pk>/", dashboardview.SectionCreateView.as_view(), name="create_section"),
    #path("show_sections/", dashboardview.SectionListView.as_view(), name="show_sections"),
    #path("update_section/<int:pk>/", dashboardview.SectionUpdateView.as_view(), name="update_section"),
    #path("section_detail/<int:pk>/", dashboardview.SectionDetailView.as_view(), name="section_detail"),
    #path("delete_section/<int:pk>/", dashboardview.SectionDeleteView.as_view(), name="delete_section"),

    # academic year related url.
    path("academic_years/", dashboardview.AcademicYearListView.as_view(), name="academic_years"),
    path("create_academic_year",dashboardview.AcademicYearCreateView.as_view(),name="create_academic_year"),
    #path("create_academic_year/", dashboardview.AcademicYearCreateView.as_view(), name="create_academic_year"),
    
    # grade related url.
    path("academic_year/<int:ay_pk>/grade/show_grade/", dashboardview.GradeListView.as_view(), name="show_grade"),


    # section related url.
    path("academic_year/<int:ay_pk>/grade/<int:grade_pk>/show_sections/", dashboardview.SectionListView.as_view(), name="show_sections"),

    #student related url
    path("academic_year/<int:ay_pk>/grade/<int:grade_pk>/section/<int:section_pk>/show_students/", dashboardview.StudentsListView.as_view(), name="show_students"),
    
    path("academic_year/<int:ay_pk>/grade/<int:grade_pk>/section/<int:section_pk>/register_parent",dashboardview.ParentCreateView.as_view(),name='register_parent')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   