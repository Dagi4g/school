from django.views.generic import CreateView,ListView,DeleteView,UpdateView,DetailView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,get_object_or_404
from django.urls import reverse_lazy
from django.db.utils import IntegrityError


from ..forms import (AnnouncementManagementForm,
                     StudentManagementForm,
                     SectionForm,GradeForm,
                     AcademicYearForm,
                     ParentForm
                     )
from ..models import (Announcement,
                      Student,
                      Parent,
                      AcademicYear,
                      Grade,Section)

class DashBoard(LoginRequiredMixin, TemplateView):
    model = Announcement
    template_name = 'dashboard/home.html'
    

'''announcement management view'''

class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementManagementForm
    template_name = 'dashboard/announcements/create_announcement.html'
    success_url = '/show_announcement/'

class DashboardAnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/announcements/show_announcement.html'
    context_object_name = 'announcements'

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

'''student management view'''

class GeneralStudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'dashboard/general_studentslist.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        grades = Grade.objects.prefetch_related('sections__students').all()
        for grade in grades:
            grade.ordered_section = grade.sections.all().order_by("name")
            
            for section in grade.ordered_section:
                section.ordered_students = section.students.all().order_by('student_name','father_name','grand_father_name')
        
        context['grades'] = grades
        return context

class AcademicYearListView(LoginRequiredMixin, ListView):
    model = AcademicYear
    template_name = 'dashboard/academic_year/show_academic_years.html'
    context_object_name = 'academicyears'

class AcademicYearCreateView(LoginRequiredMixin, CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'dashboard/academic_year/create_academic_year.html'
    success_url = '/academic_years/'

# grade related view.
class GradeListView(LoginRequiredMixin,ListView):
    model = Grade
    template_name = 'dashboard/grade/show_grades.html'
    context_object_name = 'grades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['academic_year'] = get_object_or_404(AcademicYear, pk=self.kwargs['ay_pk'])
        return context

class GradeCreateView(LoginRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'dashboard/grade/create_grade.html'

    def get_success_url(self):
        return reverse_lazy("chencha:show_grade", kwargs={"academic_year_pk": self.kwargs['ay_pk']})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['academic_year'] = get_object_or_404(AcademicYear, pk=self.kwargs['ay_pk'])
        return context

    def form_valid(self, form):
        academic_year = get_object_or_404(AcademicYear, pk=self.kwargs['ay_pk'])
        form.instance.academic_year = academic_year
        return super().form_valid(form)

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentManagementForm
    template_name = 'dashboard/student/create_student.html'
    success_url = '/show_students/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['academic_year'] = get_object_or_404(AcademicYear, pk=self.kwargs['ay_pk'])
        context['grade'] = get_object_or_404(Grade, pk=self.kwargs['grade_pk'])
        context['section'] = get_object_or_404(Section, pk=self.kwargs['section_pk'])
        return context


class SectionListView(LoginRequiredMixin,ListView):
    model = Section
    template_name = 'dashboard/section/show_sections.html'
    context_object_name = 'sections'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        academic_year = get_object_or_404(AcademicYear, pk=self.kwargs['ay_pk'])
        grade = academic_year.grades.get(pk=self.kwargs['grade_pk'])
        context['academic_year'] = academic_year
        context['grade'] = grade
        return context

    def get_queryset(self):
        section = get_object_or_404(Grade,pk=self.kwargs['grade_pk']).sections.all().order_by('name')
        return section

class SectionCreateView(LoginRequiredMixin, CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'dashboard/section/create_section.html'

    def get_success_url(self):
        return reverse_lazy("chencha:show_sections", kwargs={"grade_pk": self.kwargs['grade_pk'], "ay_pk": self.kwargs['ay_pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        academic_year = get_object_or_404(AcademicYear, pk=self.kwargs['ay_pk'])
        grade = academic_year.grades.get(pk=self.kwargs['grade_pk'])
        context['academic_year'] = academic_year
        context['grade'] = grade
        return context

    def form_valid(self, form):
        form.instance.grade = get_object_or_404(Grade, pk=self.kwargs['grade_pk'])
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            section_exists_error = "Section with this name already exists."
            context = self.get_context_data(form=form)
            context['section_exists_error'] = section_exists_error
            return self.render_to_response(context)

class StudentsListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'dashboard/student/show_students.html'
    context_object_name = 'students'

    def get_queryset(self):
        section_id = self.kwargs['section_pk']
        return Student.objects.filter(section_id=section_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['academic_year'] = get_object_or_404(AcademicYear, pk=self.kwargs['ay_pk'])
        context['section'] = get_object_or_404(Section, pk=self.kwargs['section_pk'])
        context['grade'] = get_object_or_404(Grade, pk=context['section'].grade_id)
        return context
    
class ParentCreateView(LoginRequiredMixin,CreateView):
    model = Parent
    form_class = ParentForm
    template_name = "dashboard/parent/create_parent.html"
    context_object_name = 'parent'

    def get_success_url(self):
        return reverse_lazy("chencha:register_student", kwargs={"section_pk": self.kwargs['section_pk'], "grade_pk": self.kwargs['grade_pk'], "ay_pk": self.kwargs['ay_pk']})
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['section'] = get_object_or_404(Section, pk=self.kwargs['section_pk'])
        context['grade'] = get_object_or_404(Grade, pk=self.kwargs['grade_pk'])
        context['academic_year'] = get_object_or_404(AcademicYear, pk=self.kwargs['ay_pk'])
        context['parent_exists'] = True
        return context
    
    
