from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from .models import AcademicYear,Grade

@receiver(post_save, sender=AcademicYear)
def create_related_objects(sender, instance, created, **kwargs):
    # create grades for the give academic year
    if created:
        for i in range(9, 13):
            grade_name = f'grade {i}'
            Grade.objects.create(name=grade_name, academic_year=instance)
        
        # Make all academic year not the current id the current year 
        AcademicYear.objects.exclude(id=instance.id).update(is_current=False)
        instance.is_current = True
        instance.save()

@receiver(post_delete ,sender=AcademicYear)
def handle_deleted_academic_year(sender,instance,**kwargs):
    if instance.is_current:
        if last_year := AcademicYear.objects.order_by('-id').first():
            last_year.is_current = True
            last_year.save()
        