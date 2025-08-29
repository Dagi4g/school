from django.views.generic import CreateView,ListView,DeleteView,UpdateView,DetailView,TemplateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,get_object_or_404
from django.urls import reverse_lazy
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.db import IntegrityError, transaction



from ..forms import (AnnouncementManagementForm,
                     StudentManagementForm,
                     SectionForm,GradeForm,
                     AcademicYearForm,
                     ParentForm,
                     StudentLookUpForm,
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
        academic_year = AcademicYear.objects.prefetch_related('grades__sections__students').all().order_by('-start_year')
        for year in academic_year:
            year.order_grade = year.grades.all()
            for grade in year.order_grade:
                grade.ordered_section = grade.sections.all().order_by("name")
            
                for section in grade.ordered_section:
                    section.ordered_students = section.students.all().order_by('student_name','father_name','grand_father_name')
        
        context['academic_year'] = academic_year
        return context

class AcademicYearListView(LoginRequiredMixin, ListView):
    model = AcademicYear
    template_name = 'dashboard/academic_year/show_academic_years.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['academic_year'] = self.model.objects.all().order_by('-start_year')

        return context

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
        grade = get_object_or_404(Grade, pk=self.kwargs['grade_pk'])
        form.instance.grade = grade
        try:
            return super().form_valid(form)
        except Exception as e:
            form.add_error(None, "A section with this name already exists in this grade.")
            return self.form_invalid(form)

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


class StudentParentCreateView(TemplateView):
    template_name = "dashboard/student/create_student.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = get_object_or_404(Section, id=self.kwargs.get('section_pk'))
        context['section'] = section
        context['parent_form'] = ParentForm()
        context['student_form'] = StudentManagementForm()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        parent_form = ParentForm(request.POST)
        student_form = StudentManagementForm(request.POST)

        if parent_form.is_valid() and student_form.is_valid():
            parent_data = parent_form.cleaned_data
            try:
                with transaction.atomic():
                    # Create or get the parent
                    parent, created = Parent.objects.get_or_create(
                        name=parent_data['name'],
                        father_name=parent_data['father_name'],
                        defaults={
                            'relation_ship': parent_data.get('relation_ship'),
                            'email': parent_data.get('email'),
                            'phone': parent_data.get('phone'),
                            'work': parent_data.get('work'),
                            'income': parent_data.get('income'),
                        }
                    )
            except IntegrityError:
                # If duplicate slips through, fetch existing parent
                parent = Parent.objects.get(
                    name=parent_data['name'],
                    father_name=parent_data['father_name']
                )

            # Create the student object but don't save yet
            student = student_form.save(commit=False)
            student.parent = parent
            section = get_object_or_404(Section, id=self.kwargs.get('section_pk'))
            student.section = section
            student.academic_year = section.grade.academic_year

            # Check unique constraint before saving
            try:
                student.validate_unique()
                student.save()
                return redirect('chencha:student_list')
            except ValidationError as e:
                # Add errors to form to show in UI
                student_form.add_error(None, 'ይህ ተማር ከዝህ በፊት ተመዝግቧል ። እባክዎ ሌላ ተማር ይመዝግቡ።')

        # Re-render the page with errors if forms are invalid or duplicate
        context = {
            'parent_form': parent_form,
            'student_form': student_form,
        }
        return render(request, self.template_name, context)

class SectionLookUpView(FormView):
    template_name = 'students/section_lookup.html'
    form_class = StudentLookUpForm
    
    def form_valid(self,form):
        name = form.cleaned_data['name']
        father_name = form.cleaned_data['father_name']
        grand_father_name = form.cleaned_data['grand_father_name']
        grade = form.cleaned_data['grade']
        current_academic_year = AcademicYear.objects.get(is_current=True)
        
        try :
            student = Student.objects.get(
                student_name__icontains=name.strip().title(),
                father_name__icontains=father_name.strip().title(),
                grand_father_name__icontains=grand_father_name.strip().title(),
                section__grade__name=grade,
                section__grade__academic_year=current_academic_year
                
            )
            return render(
                self.request,
                self.template_name,
                {'section':student.section,'student':student,'form':form},
            )
        except Student.DoesNotExist:
            return render(self.request,
                        self.template_name,
                        {'error':f"Oops! We couldn’t locate a student with the information you provided for {grade}, {current_academic_year}. Please double-check and try again.",'form': form}
                        )