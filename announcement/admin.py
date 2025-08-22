from django.contrib import admin
from . import models

admin.site.register(models.Announcement)
admin.site.register(models.ParentForm)
admin.site.register(models.AcademicYear)
admin.site.register(models.Grade)
admin.site.register(models.Section)
admin.site.register(models.Student)
