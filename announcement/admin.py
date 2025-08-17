from django.contrib import admin
from . import models

admin.site.register(models.Announcement)
admin.site.register(models.Student)
admin.site.register(models.Parent)
admin.site.register(models.AcademicYear)
admin.site.register(models.Grade)
admin.site.register(models.Section)
