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

import re
import csv
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
import os

def split_fullname(fullname):
    """Split full name into student, father, grandfather."""
    parts = fullname.strip().split()
    if len(parts) >= 3:
        return parts[0], parts[1], " ".join(parts[2:])
    elif len(parts) == 2:
        return parts[0], parts[1], ""
    else:
        return parts[0], "", ""

def iter_block_items(parent):
    """Yield paragraphs and tables in order."""
    for child in parent.element.body:
        if child.tag.endswith("p"):
            yield Paragraph(child, parent)
        elif child.tag.endswith("tbl"):
            yield Table(child, parent)

def save_students_to_csv(docx_path, output_folder="."):
    doc = Document(docx_path)
    current_school = None
    students = []

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = block.text.strip()
            # Treat paragraph as school name if not empty and not header
            if text and "Name of student" not in text and not text[0].isdigit():
                # Save previous school's data if exists
                if current_school and students:
                    filename = os.path.join(output_folder, f"{current_school}.csv")
                    with open(filename, "w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(["Student Name", "Father Name", "Grandfather Name", "Sex", "Age"])
                        writer.writerows(students)
                    print(f"Saved {len(students)} students to {filename}")
                    students = []

                current_school = text

        elif isinstance(block, Table):
            for row in block.rows[1:]:  # skip header
                cells = [c.text.strip() for c in row.cells]
                if not cells or not cells[0].isdigit():
                    continue

                fullname = cells[1]
                sex = cells[2].strip().upper()
                age = re.sub(r"\D", "", cells[3])
                age = int(age) if age.isdigit() else ""

                student_name, father_name, grandfather_name = split_fullname(fullname)
                students.append([student_name, father_name, grandfather_name, sex, age])

    # Save last school's data
    if current_school and students:
        filename = os.path.join(output_folder, f"{current_school}.csv")
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Student Name", "Father Name", "Grandfather Name", "Sex", "Age"])
            writer.writerows(students)
        print(f"Saved {len(students)} students to {filename}")

if __name__ == "__main__":
    import sys 
    if len(sys.argv) != 2:
        print("Usage: python import_marks.py <path_to_word_document>")
        sys.exit(1)
    
    doc_path = sys.argv[1]
    save_students_to_csv(doc_path, output_folder=".")
    print("Import completed!")

