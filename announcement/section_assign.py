import random
import string
from collections import defaultdict, Counter
from django.core.exceptions import ImproperlyConfigured
from .models import AutoSectionGrade


class SectionAssigner:
    def __init__(self, students: list[dict], num_sections: int):
        if not isinstance(students, list):
            raise TypeError("students must be a list of dictionaries")
        if not isinstance(num_sections, int):
            raise TypeError("number of sections must be an integer")
        if num_sections <= 0:
            raise ValueError("number ofsections must be greater than 0")

        self.students = students
        self.num_sections = num_sections
        self.sections = [[] for _ in range(num_sections)]
        self.unassigned_students = []
        self.school_groups = defaultdict(list)
        self.stats = {}

    def group_by_school(self):
        for s in self.students:
            if 'previous_school' not in s or 'sex' not in s:
                self.unassigned_students.append(s)
                continue 
            self.school_groups[s['previous_school']].append(s)

        for school in self.school_groups:
            random.shuffle(self.school_groups[school])
            ratio = len(self.school_groups[school]) / len(self.students)
            print(f'[INFO] School: {school} - {len(self.school_groups[school])} students ({ratio*100:.2f}%)')

    def calculate_gender_ratio(self):
        total_students = len(self.students)
        if total_students == 0:
            raise ValueError("no student in the database or all student have been assigned a section")

        male_count = sum(1 for s in self.students if s.get('sex') == 'm')
        female_count = total_students - male_count
        male_ratio = male_count / total_students
        female_ratio = female_count / total_students

        print(f'[INFO] Total students: {total_students} | '
            f'Males: {male_count} ({male_ratio*100:.2f}%) | '
            f'Females: {female_count} ({female_ratio*100:.2f}%)\n')

        return total_students, male_count, female_count, male_ratio, female_ratio

    def assign_students(self):
        total_students, male_count, female_count, male_ratio, female_ratio = self.calculate_gender_ratio()

        for school, s_list in self.school_groups.items():
            
            # Safely categorize students, defaulting to "unscored"
            top = [s for s in s_list if s.get('minstry_score') is not None and s['minstry_score'] >= 75]
            avg = [s for s in s_list if s.get('minstry_score') is not None and 65 <= s['minstry_score'] < 75]
            strug = [s for s in s_list if s.get('minstry_score') is not None and s['minstry_score'] < 65]
            unscored = [s for s in s_list if s.get('minstry_score') is None]

            # print(f'[INFO] Assigning students from school: {school}')
            # print(f'  Top: {len(top)}, Average: {len(avg)}, Struggling: {len(strug)}, Unscored: {len(unscored)}')

            # Assign students per category
            for category_name, category in zip(
                ['Top', 'Average', 'Struggling', 'Unscored'],
                [top, avg, strug, unscored]
            ):
                for s in category:
                    idx = min(range(self.num_sections), key=lambda i: len(self.sections[i]))
                    section = self.sections[idx]

                    male_in_sec = sum(1 for stu in section if stu.get('sex') == 'm')
                    female_in_sec = len(section) - male_in_sec
                    total_in_sec = len(section) + 1

                    expected_male = male_ratio * total_in_sec
                    expected_female = female_ratio * total_in_sec

                    if s.get('sex', '').lower() == 'm' and male_in_sec + 1 > expected_male + 1:
                        idx = min(range(self.num_sections), key=lambda i: len(self.sections[i]))
                    if s.get('sex', '').lower() == 'f' and female_in_sec + 1 > expected_female + 1:
                        idx = min(range(self.num_sections), key=lambda i: len(self.sections[i]))

                    self.sections[idx].append(s)

        if self.unassigned_students:
            print(f'\n[WARNING] {len(self.unassigned_students)} students missing required info. Assigning them to smallest sections.')
            for s in self.unassigned_students:
                idx = min(range(self.num_sections), key=lambda i: len(self.sections[i]))
                self.sections[idx].append(s)

        for sec in self.sections:
            random.shuffle(sec)
        random.shuffle(self.sections)


    def calculate_statistics(self):
        print(self.school_groups.items())
        total_students = len(self.students)
        male_count = sum(1 for s in self.students if s.get('sex').lower() == 'm')
        female_count = total_students - male_count
        male_ratio = round(100 * male_count / total_students, 2) if total_students else 0
        female_ratio = round(100 * female_count / total_students, 2) if total_students else 0
        
        
        stats = {
            "total_students": total_students,
            "total_sections": self.num_sections,
            "gender_ratio": {
                "male": male_count,
                "female": female_count,
                "male_ratio": male_ratio,
                "female_ratio": female_ratio
            },
            "school_counts": {
                school: {
                    'count': len(students), 
                    'ratio': round((len(students) / total_students) * 100, 2) if total_students else 0
                }
                for school, students in self.school_groups.items() 
            },
            "sections": {}
        }
        
        

        alphabet = string.ascii_uppercase
        for i, sec in enumerate(self.sections):
            label = alphabet[i] if i < len(alphabet) else f"Sec{i+1}"

            male_sec = sum(1 for s in sec if s.get('sex').lower() == 'm')
            female_sec = len(sec) - male_sec
            top_sec = sum(1 for s in sec if s.get('minstry_score') is not None and s['minstry_score'] >= 75)
            avg_sec = sum(1 for s in sec if s.get('minstry_score') is not None and 65 <= s['minstry_score'] < 75)
            strug_sec = sum(1 for s in sec if s.get('minstry_score') is not None and s['minstry_score'] < 65)
            unscored_sec = sum(1 for s in sec if s.get('minstry_score') is None)
            school_counts = Counter([s.get('previous_school', 'Unknown') for s in sec])

            stats["sections"][label] = {
                "total": len(sec),
                "males": male_sec,
                "females": female_sec,
                "top": top_sec,
                "average": avg_sec,
                "struggling": strug_sec,
                "unscored": unscored_sec,
                "schools": dict(school_counts),
                "school_ratios": {
                    school: round((count / len(sec)) * 100, 2) if len(sec) else 0
                    for school, count in school_counts.items()
                },
                "gender_ratio": {
                    "male_ratio": round((male_sec / len(sec)) * 100, 2) if len(sec) > 0 else 0,
                    "female_ratio": round((female_sec / len(sec)) * 100, 2) if len(sec) > 0 else 0
                }
            }

        self.stats = stats
        return stats


    def run(self):
        self.group_by_school()
        self.assign_students()
        stats = self.calculate_statistics()
        return self.sections, self.stats


def assign_and_save(model,num_section,students):
    """Assigns students from the given model to sections and updates their section assignment in the database.

    Retrieves all students, assigns them to sections using the assigns function, and updates each student's section field in the database.

    Args:
        model: The Django model representing students.
        num_section: The number of sections to assign students to.
    """
    if not issubclass(model,AutoSectionGrade):
        raise ImproperlyConfigured("assign_and_save function expects the AutoSectionGrade model.")
    
    assigner = SectionAssigner(students, num_sections=num_section)
    sections, stats = assigner.run()
    
    from .models import AutoGradeStat
    
    stat_obj, created = AutoGradeStat.objects.get_or_create(id=1)
    stat_obj.stats = stats
    stat_obj.save()
    for idx, section_students in enumerate(sections):
        section_name = chr(65+ idx)
        for student in section_students:
            model.objects.filter(id=student['id']).update(section=section_name, stats=stat_obj)





