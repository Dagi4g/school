from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .dashboard import dashboardview
from . import views

app_name = 'chencha'

user_urls = [
    path("", views.home, name="home"),
    path("announcements/", views.AnnouncementListView.as_view(), name="announcement_list"),
    path("about_us/", views.about_us, name="about_us"),

]

dashboard_urls = [
    path ("dashboard/", dashboardview.DashBoard.as_view(), name="dashboard"),
    path("create_announcement/", dashboardview.AnnouncementCreateView.as_view(), name="create_announcement"),
    path("show_announcement/", dashboardview.DashboardAnnouncementListView.as_view(template_name='dashboard/announcements/show_announcement.html'), name="show_announcement"),
    path("update_announcement/<int:pk>/", dashboardview.AnnouncementUpdateView.as_view(), name="update_announcement"),
    path("announcement_detail/<int:pk>/", dashboardview.AnnouncementDetailView.as_view(), name="announcement_detail"),
    path("delete_announcement/<int:pk>/", dashboardview.AnnouncementDeleteView.as_view(), name="delete_announcement"),
]

urlpatterns = [
    path('assign',views.SectionAssignerView.as_view(),name='assign'),
    path('autograde_create',views.AutoGradeSectionCreateView.as_view(),name='autograde_create'),
    path('student_nosection',views.show_students_nosection,name='student_nosection'),
    path('list_students',views.show_sections,name='show_sections'),
    path('look_up/',dashboardview.SectionLookUpView.as_view(),name='lookup'),
    
    # the school dashboard.
    
    # student related dashboard view
    path("students/", dashboardview.GeneralStudentListView.as_view(), name="student_list"),
    path("academic_year/<int:ay_pk>/grade/<int:grade_pk>/section/<int:section_pk>/register_student/",dashboardview.StudentParentCreateView.as_view(),name="register_student"),
    # section related views
    path("academic_year/<int:ay_pk>/grade/<int:grade_pk>/create_section", dashboardview.SectionCreateView.as_view(), name="create_section"),
    

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

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + user_urls + dashboard_urls