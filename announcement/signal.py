from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AcademicYear,Grade

@receiver(post_save, sender=AcademicYear)
def create_related_objects(sender, instance, created, **kwargs):
    if created:
        for i in range(9, 13):
            grade_name = f'grade {i}'
            Grade.objects.create(name=grade_name, academic_year=instance)