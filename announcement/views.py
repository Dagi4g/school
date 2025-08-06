from django.shortcuts import render

def announcement_list(request):
    return render(request, 'announcement/announcement_list.html')