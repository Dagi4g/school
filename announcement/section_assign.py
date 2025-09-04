import random
from collections import defaultdict
from django.core.exceptions import ImproperlyConfigured
from .models import AutoSectionGrade

def assigns(students, num_sections) -> list[list[dict]]:
    """
    Assign students to sections based on:
    1. School ratio
    2. Performance categories (Top / Average / Struggling)
    3. Gender balance (softly, not strict)
    
    Prints assignment info in terminal.
    """
    if not isinstance(students, list):
        raise TypeError("students must be a list of dictionaries")
    if num_sections <= 0:
        raise ValueError("num_sections must be greater than 0")

    sections = [[] for _ in range(num_sections)]
    unassigned_students = []

    # Group students by school
    school_groups = defaultdict(list)
    for s in students:
        if 'previous_school' not in s or 'minstry_score' not in s or 'sex' not in s:
            unassigned_students.append(s)
            continue
        school_groups[s['previous_school']].append(s)

    # Shuffle each school's students for randomness
    for school in school_groups:
        random.shuffle(school_groups[school])
        school_ratio = len(school_groups[school]) / len(students)
        print(f'[INFO] School: {school} - {len(school_groups[school])} students ({school_ratio*100:.2f}%)')

    # Global gender ratio
    total_students = len(students)
    if total_students == 0:
        raise ValueError("no student in the database")
    male_count = sum(1 for s in students if s.get('sex') == 'm')
    female_count = total_students - male_count
    male_ratio = male_count / total_students
    female_ratio = female_count / total_students
    print(f'[INFO] Total students: {total_students} | Males: {male_count} ({male_ratio*100:.2f}%) | Females: {female_count} ({female_ratio*100:.2f}%)\n')

    # Assign students category by category
    for school, s_list in school_groups.items():
        top_students = [s for s in s_list if s['minstry_score'] >= 75]
        average_students = [s for s in s_list if 65 <= s['minstry_score'] < 75]
        struggling_students = [s for s in s_list if s['minstry_score'] < 65]

        print(f'[INFO] Assigning students from school: {school}')
        print(f'  Top: {len(top_students)}, Average: {len(average_students)}, Struggling: {len(struggling_students)}')

        for category_name, category in zip(['Top', 'Average', 'Struggling'], [top_students, average_students, struggling_students]):
            for s in category:
                idx = min(range(num_sections), key=lambda i: len(sections[i]))
                section = sections[idx]
                male_in_section = sum(1 for stu in section if stu['sex'] == 'm')
                female_in_section = len(section) - male_in_section
                total_in_section = len(section) + 1

                expected_male = male_ratio * total_in_section
                expected_female = female_ratio * total_in_section

                # Only skip if it drastically violates ratio, otherwise assign
                if s['sex'].lower() == 'm' and male_in_section + 1 > expected_male + 1:
                    idx = min(range(num_sections), key=lambda i: len(sections[i]))
                if s['sex'].lower() == 'f' and female_in_section + 1 > expected_female + 1:
                    idx = min(range(num_sections), key=lambda i: len(sections[i]))

                sections[idx].append(s)

    # Any unassigned students (missing data) go to sections with least students
    if unassigned_students:
        print(f'\n[WARNING] {len(unassigned_students)} students missing required info. Assigning them to smallest sections.')
        for s in unassigned_students:
            idx = min(range(num_sections), key=lambda i: len(sections[i]))
            sections[idx].append(s)

    # Shuffle sections for randomness
    for sec in sections:
        random.shuffle(sec)
    random.shuffle(sections)

    import string
    from collections import Counter

    print('\n[INFO] Final Section Distribution:')
    alphabet = string.ascii_uppercase
    for i, sec in enumerate(sections):
        male_sec = sum(1 for s in sec if s.get('sex') == 'm')
        female_sec = len(sec) - male_sec

        top_sec = sum(1 for s in sec if s.get('minstry_score', 0) >= 75)
        avg_sec = sum(1 for s in sec if 65 <= s.get('minstry_score', 0) < 75)
        strug_sec = sum(1 for s in sec if s.get('minstry_score', 0) < 65)

        section_label = alphabet[i] if i < len(alphabet) else f"Sec{i+1}"
        print(
            f'\n  Section {section_label}: {len(sec)} students | '
            f'Males: {male_sec} ({male_sec/len(sec)*100:.2f}%), '
            f'Females: {female_sec} ({female_sec/len(sec)*100:.2f}%) | '
            f'Top: {top_sec}, Avg: {avg_sec}, Struggling: {strug_sec}'
        )

        # Calculate school ratios inside this section
        schools_in_sec = [s.get('previous_school', 'Unknown') for s in sec]
        school_counts = Counter(schools_in_sec)
        for school, count in school_counts.items():
            ratio = (count / len(sec)) * 100
            print(f'    {school}: {count} ({ratio:.2f}%)')
            
        from collections import Counter

        # Prepare statistics
        stats = {
            "total_students": total_students,
            "total_sections": num_sections,
            "gender_ratio": {"male": male_count, "female": female_count, 'male_ratio': round(100*male_ratio, 2), 'female_ratio': round(100*female_ratio, 2)},
            "school_counts": {school: {'count': len(students), 'ratio': round((len(students) / total_students) * 100, 2)} for school, students in school_groups.items()},
            "sections": {}
        }

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for i, sec in enumerate(sections):
            section_label = alphabet[i] if i < len(alphabet) else f"Sec{i+1}"
            male_sec = sum(1 for s in sec if s.get('sex') == 'm')
            female_sec = len(sec) - male_sec
            top_sec = sum(1 for s in sec if s.get('minstry_score', 0) >= 75)
            avg_sec = sum(1 for s in sec if 65 <= s.get('minstry_score', 0) < 75)
            strug_sec = sum(1 for s in sec if s.get('minstry_score', 0) < 65)

            schools_in_sec = [s.get('previous_school', 'Unknown') for s in sec]
            school_counts = Counter(schools_in_sec)

            stats["sections"][section_label] = {
                "total": len(sec),
                "males": male_sec,
                "females": female_sec,
                "top": top_sec,
                "average": avg_sec,
                "struggling": strug_sec,
                "schools": dict(school_counts),
                "school_ratios": {school: round((count / len(sec)) * 100, 2) for school, count in school_counts.items()},
                'gender_ratio': {
                    'male_ratio': round((male_sec / len(sec)) * 100, 2),
                    'female_ratio': round((female_sec / len(sec)) * 100, 2)
                }
            }

    return sections,stats


def assign_and_save(model,num_section):
    """Assigns students from the given model to sections and updates their section assignment in the database.

    Retrieves all students, assigns them to sections using the assigns function, and updates each student's section field in the database.

    Args:
        model: The Django model representing students.
        num_section: The number of sections to assign students to.
    """
    if not issubclass(model,AutoSectionGrade):
        raise ImproperlyConfigured("assign_and_save function expects the AutoSectionGrade model.")
    students = list(model.objects.all().values('id','student_name', 'previous_school', 'minstry_score', 'sex'))
    sections, stats = assigns(students,num_section)

    for idx, section_students in enumerate(sections):
        section_name = chr(65+ idx)
        for student in section_students:
            model.objects.filter(id=student['id']).update(section=section_name)
    return stats





