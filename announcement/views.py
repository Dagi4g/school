from django.shortcuts import render
from django.views.generic import ListView,CreateView,DetailView,TemplateView,FormView
from django.http import HttpResponse


from .forms import AutoSectionGradeForm,SectionInputForm,StudentLookUpForm
from .models import Announcement,AutoSectionGrade
from .section_assign import assign_and_save

def home(request):
    return render(request, 'announcement/home.html')

def about_us(request):
    
    return render(request, 'announcement/about_us.html')

class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcement/announcement_list.html'
    context_object_name = 'announcements'

class AutoGradeSectionCreateView(CreateView):
    model = AutoSectionGrade
    form_class = AutoSectionGradeForm
    template_name ='autograde/add_student.html'
    success_url = 'student_nosection'


class SectionAssignerView(FormView):
    template_name = "autograde/assigner.html"
    form_class = SectionInputForm
    success_url = 'list_students'
    

    def form_valid(self, form):
        section_number = form.cleaned_data["section_number"]
        try:
            stats = assign_and_save(AutoSectionGrade, section_number)
            self.request.session['sections_stats'] = stats  # Store stats in session
        except Exception as e:
            form.add_error(None, f"{e}")
            return super().form_invalid(form)
        return super().form_valid(form)


    

def show_sections(request):
    # Get only students who have a section assigned
    stats = request.session.get('sections_stats', {})
    sections = AutoSectionGrade.objects.exclude(section__isnull=True).exclude(section='').values('section', 'student_name', 'previous_school', 'minstry_score', 'sex').order_by('section')
    section_dict = {}
    for s in sections:
        section_dict.setdefault(s['section'], []).append(s)
    print(stats)
        
    return render(request, 'autograde/sections.html', {'section_dict': section_dict,'stats': stats})
    
def show_students_nosection(request):
    # Get only students who have no section assigned
    sections = AutoSectionGrade.objects.filter(section__isnull=True).values('section', 'student_name', 'previous_school', 'minstry_score', 'sex').order_by('student_name')

    len_student = len(sections)
    section_dict = {}
    for s in sections:
        section_dict.setdefault(s['section'], []).append(s)
    

    return render(request, 'autograde/student_nosection.html', {'section_dict': section_dict, 'len_student': len_student})

class SectionLookUpView(FormView):
    template_name = 'students/section_lookup.html'
    form_class = StudentLookUpForm
    
    def form_valid(self,form):
        name = form.cleaned_data['name']
        father_name = form.cleaned_data['father_name']
        grand_father_name = form.cleaned_data['grand_father_name']
        grade = form.cleaned_data['grade']
        
        try :
            student = AutoSectionGrade.objects.get(
                student_name=name.strip().title(),
                father_name=father_name.strip().title(),
                grandfather_name=grand_father_name.strip().title(),
                grade=grade.strip()
            )
            if student.section:
                return render(
                self.request,
                self.template_name,
                {'section':student.section,'student':student,'form':form},
            )
            else:
                return render(
                    self.request,
                    self.template_name,
                    {'student_has_no_section':'ይህ ተማር ትመዝግባል ነገር ግን ክፍል አልተሰጠዉም። እባክህ አስተዳደሩን ያነጋግሩ።','form':form},
                )
        except AutoSectionGrade.DoesNotExist:
            return render(self.request,
                        self.template_name,
                        {'error':f"ውይ! ከ {grade[6:]} ክፍል ያቀረቡትን መረጃ የያዘ ተማሪ ማግኘት አልቻልንም። እባክህ ደግመህ አረጋግጥ እና እንደገና ሞክር።", 'form': form}
                        )