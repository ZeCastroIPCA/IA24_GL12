# Import contraint lybrary
from constraint import *

# Function to read and parse the file
def parse_file(file_path):
    data = {'tr': {}, 'dsd': {}, 'cc': {}}
    current_section = None  # To track the section we are reading

    # Open the file for reading
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading and trailing whitespace
            print(line)
            # Skip header section or any comment lines
            if line.startswith("##") or line.startswith("—") or not line:
                continue

            # Check for section labels
            if line.startswith("#tr"):
                current_section = 'tr'  # Timeslot restrictions
                continue
            elif line.startswith("#dsd"):
                current_section = 'dsd'  # Courses assigned to lecturers
                continue
            elif line.startswith("#cc"):
                current_section = 'cc'  # Courses assigned to classes
                continue

            # Parse based on the current section
            if current_section == 'tr':
                # Split line by spaces, first element is the lecturer, rest are the timeslots
                parts = line.split()
                lecturer = parts[0]
                timeslots = list(map(int, parts[1:]))  # Convert timeslots to integers
                data['tr'][lecturer] = timeslots

            elif current_section == 'dsd':
                # Split line by spaces, first element is the lecturer, rest are the courses
                parts = line.split()
                lecturer = parts[0]
                courses = parts[1:]  # Courses are strings (e.g., UC11, UC21)
                data['dsd'][lecturer] = courses

            elif current_section == 'cc':
                # Split line by spaces, first element is the class, rest are the courses
                parts = line.split()
                class_name = parts[0]
                courses = parts[1:]  # Courses are strings (e.g., UC11, UC12)
                data['cc'][class_name] = courses

    return data

# Read the file
file_path = './dataset.txt'  # Replace with your actual file path
parsed_data = parse_file(file_path)

# Output the parsed data for verification
print("Timeslot Restrictions (tr):")
for lecturer, timeslots in parsed_data['tr'].items():
    print(f"{lecturer}: {timeslots}")

print("\nLecturer-Course Assignments (dsd):")
for lecturer, courses in parsed_data['dsd'].items():
    print(f"{lecturer}: {courses}")

print("\nCourse-Class Assignments (cc):")
for class_name, courses in parsed_data['cc'].items():
    print(f"{class_name}: {courses}")

# Create a dictionary for weekly classes per lecturer
# In the example all courses have two classes per week
weekcls = {}
for lecturer, courses in parsed_data['dsd'].items():
    if lecturer not in weekcls:
        weekcls[lecturer] = []
    for course in courses:
        weekcls[lecturer].append(f'{course}a')
        weekcls[lecturer].append(f'{course}b')


# Get the list of all courses, all classes/lessons, and all lessons by study_plan/year (turma)
course_list = []
lesson_list = []
study_plan = {}
for class_name, courses in parsed_data['cc'].items():
    if class_name not in study_plan:
        study_plan[class_name] = []
    for course in courses:
      course_list.append(f'{course}')
      lesson_list.append(f'{course}a')
      lesson_list.append(f'{course}b')
      study_plan[class_name].append(f'{course}a')
      study_plan[class_name].append(f'{course}b')

print(weekcls)
print(course_list)
print(lesson_list)
print(study_plan)

# Initiate the solver
ctt_problem = Problem()

# Add variables and ist domain
tt_slots = list(range(1,21))
for lecturer, tr_slots in parsed_data['tr'].items():
    av_slots = [item for item in tt_slots if item not in tr_slots]
    ctt_problem.addVariables(weekcls[lecturer], av_slots)
    print(lecturer, ': ', weekcls[lecturer], ' — ', av_slots)

# CONSTRAINTS FUNCTIONS

# Constraint that returns True if there is no more than 2 lessons at same time, False otherwise
def atmost_two(*values):
    for v in set(values):
        if values.count(v) > 2:
            return False
    return True

# Constraint that returns True if the are not in the same day, False otherwise
def const_diff_day(*values):
    if (values[1]-1) // 4 > (values[0]-1) // 4:
        return True
    return False

# constraints

# Studyplan: limits simultaneous lessons
for sp in study_plan:
    ctt_problem.addConstraint(AllDifferentConstraint(), study_plan[sp])


# Profs: limits simultaneous lessons
for p in weekcls:
    ctt_problem.addConstraint(AllDifferentConstraint(), weekcls[p])

# courses: 24h interval between classes of same course
for uc in course_list:
    # ctt_problem.addConstraint(FunctionConstraint(const_diff_day), [f'{uc}a', f'{uc}b'])
    ctt_problem.addConstraint(lambda a, b: (b-1) // 4 > (a-1) // 4, [f'{uc}a', f'{uc}b'])

# Classrooms: only two classrooms available
ctt_problem.addConstraint(FunctionConstraint(atmost_two), lesson_list)

# Get ONE solution
ctt_sol = ctt_problem.getSolution()

# Print solution
if ctt_sol:
    sorted_ucs_by_slot_list = sorted(ctt_sol.items(), key=lambda x:x[1])
    sorted_ucs_by_slot = dict(sorted_ucs_by_slot_list)
    for sp in study_plan:
        print(sp, end=': ' )
        for uc in sorted_ucs_by_slot:
            if uc in study_plan[sp]:
                print(ctt_sol[uc],end=':')
                print(uc, end=' ')
        print()

