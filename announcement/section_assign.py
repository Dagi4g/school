import random
from collections import defaultdict

def assigns(students, num_sections) -> list[list[dict]]:
    """
    Assign students to sections based on:
    1. School ratio relative to total students
    2. Performance ratio (Top/Average/Struggling based on score thresholds)
    3. Gender ratio (match class ratio with global ratio of male/female)
    
    Handles exceptions per student, logs them, and continues processing.
    """

    if not isinstance(students, list):
        raise TypeError("students must be a list of dictionaries")
    if num_sections <= 0:
        raise ValueError("num_sections must be greater than 0")

    sections = [[] for _ in range(num_sections)]
    error_log = []

    # 1. Group students by school
    school_groups = defaultdict(list)
    for s in students:
        try:
            if 'previous_school' not in s or 'minstry_score' not in s or 'sex' not in s:
                raise KeyError("Missing 'school', 'score', or 'sex'")
            school_groups[s['previous_school']].append(s)
        except Exception as e:
            error_log.append((s, str(e)))
            continue

    # Sort each school's students by score
    for school in school_groups:
        try:
            school_groups[school].sort(key=lambda x: x['minstry_score'], reverse=True)
        except Exception as e:
            error_log.append((f"School {school}", str(e)))
    

    total_students = sum(len(lst) for lst in school_groups.values())
    print(total_students)
    if total_students == 0:
        raise ValueError("No valid students to assign")

    # --- Global gender ratio ---
    male_count = sum(1 for s in students if s.get('sex') == 'm')
    female_count = total_students - male_count
    male_ratio = male_count / total_students
    female_ratio = female_count / total_students
    print(f"Global gender ratio: M={male_ratio:.2f}, F={female_ratio:.2f}")

    # 2. For each school, split into categories
    for school, s_list in school_groups.items():
        n = len(s_list)
        if n == 0:
            continue

        # Performance categorization
        top_students = [s for s in s_list if s['minstry_score'] >= 75]
        average_students = [s for s in s_list if 65 <= s['minstry_score'] < 75]
        struggling_students = [s for s in s_list if s['minstry_score'] < 65]

        print(f"{school}: top={len(top_students)}, avg={len(average_students)}, struggle={len(struggling_students)}")

        # Fair distribution across sections
        base = n // num_sections
        remainder = n % num_sections
        students_per_section = [base + (1 if i < remainder else 0) for i in range(num_sections)]

        # Assign round-robin while keeping gender balance
        category_lists = [top_students, average_students, struggling_students]
        idx = 0
        # Assign round-robin while keeping gender balance
        for category in category_lists:
            for s in category:
                assigned = False
                for _ in range(num_sections):  # try each section once
                    idx_mod = idx % num_sections
                    section = sections[idx_mod]

                    male_in_section = sum(1 for stu in section if stu['sex'] == 'm')
                    female_in_section = len(section) - male_in_section
                    total_in_section = len(section) + 1  # including this student

                    expected_male = male_ratio * total_in_section
                    expected_female = female_ratio * total_in_section

                    if (s['sex'].lower() == 'm' and male_in_section + 1 <= expected_male + 1) or \
                    (s['sex'].lower() == 'f' and female_in_section + 1 <= expected_female + 1):
                        section.append(s)
                        students_per_section[idx_mod] -= 1
                        assigned = True
                        idx += 1
                        break
                    idx += 1

                # If not assigned due to strict ratio, just put them in the section with the least students
                if not assigned:
                    min_idx = min(range(num_sections), key=lambda i: len(sections[i]))
                    sections[min_idx].append(s)
                    students_per_section[min_idx] -= 1
            
    if error_log:
        print("\nThe following errors occurred during assignment:")
        for item, msg in error_log:
            print(f"  Student/Data: {item}, Error: {msg}")

    random.shuffle(sections)
    return sections

def assign_and_save(model,num_section):
    students = list(model.objects.all().values('id','student_name', 'previous_school', 'minstry_score', 'sex'))
    sections = assigns(students,num_section)
    
    for idx, section_students in enumerate(sections):
        section_name = chr(65+ idx)
        for student in section_students:
            model.objects.filter(id=student['id'],).update(section=section_name)
        




