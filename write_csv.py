# Copyright 2025 Dagim Genene
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import os
import django

# Setup Django environment if running as standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chencha_school.settings")
django.setup()

from announcement.models import AutoSectionGrade

# Path to your CSV file

# Open and read CSV
def read_csv(csv_file_path):
    school_name = f'{csv_file_path.split(os.sep)[-1].replace(".csv","")}'
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # process each row and return the data
            yield row['Student Name'], row['Father Name'], row['Grandfather Name'], row['Sex'], row['Age'], school_name, 'grade 9'


def write_to_db(file_path,):
    data = list(read_csv(file_path))
    for student_name, father_name, grandfather_name, sex, age, school_name, grade in data:
        student, created = AutoSectionGrade.objects.update_or_create(
            student_name=student_name.title(),
            father_name=father_name.title(),
            grandfather_name=grandfather_name.title(),
            sex=sex.title(),
            age=age,
            previous_school=school_name.title(),
            grade=grade.title()
        )
        print(f"{'Created' if created else 'Updated'}: {student}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) <= 2:
        print("Usage: python write_csv.py <path_to_csv_file>")
        sys.exit(1)

    for file in sys.argv[1:]:
        write_to_db(file)