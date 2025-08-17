from django.shortcuts import render
from .models import Announcement, Student
from .forms import SectionLookupForm



def home(request):
    return render(request, 'announcement/home.html')

def about_us(request):
    return render(request, 'announcement/about_us.html')

def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'announcement/announcement_list.html', {'announcements': announcements})

def student_section_lookup(request):
    section = None
    not_found = False

    if request.method == 'POST':
        form = SectionLookupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'].strip().title()
            last_name = form.cleaned_data['last_name'].strip().title()
            grade = form.cleaned_data['grade']

            try:
                student = Student.objects.get(
                    first_name=first_name,
                    last_name=last_name,
                    grade=grade
                    
                )
                section = student.section
            except Student.DoesNotExist:
                not_found = True

    else:
        form = SectionLookupForm()

    return render(request, 'announcement/student_section_lookup.html', {
        'form': form,
        'section': section,
        'not_found': not_found
    })
