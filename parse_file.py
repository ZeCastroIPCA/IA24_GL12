def parse_file(file_path):

    # Initialize data dictionary
    data = {
        'projects': {},
        'precedence': {},
        'duration_resources': {},
        'resource_availability': {}
    }
    current_section = None

    # Open the file
    with open(file_path, 'r') as file:
        for line in file:
            # Remove leading and trailing whitespaces
            line = line.strip()

            # Skip empty lines and comments
            if line.startswith("*") or not line:
                continue

            # Check for section headers
            if line.startswith("#Projects summary"):
                current_section = 'projects'
                continue
            elif line.startswith("#Precedence relations"):
                current_section = 'precedence'
                continue
            elif line.startswith("#Duration and resources"):
                current_section = 'duration_resources'
                continue
            elif line.startswith("#Resource availability"):
                current_section = 'resource_availability'
                continue

            # Skip lines with keywords
            if any(keyword in line for keyword in ["pronr.", "#jobs", "#modes", "resource", "qty", "jobnr.", "#successors", "mode", "duration"]):
                continue

            # print("Line: ", line)
            # print("Current section: ", current_section)

            # Parse data based on the current section
            if current_section == 'projects':
                parts = line.split()
                project_id = int(parts[0])
                data['projects'][project_id] = {
                    'num_jobs': int(parts[1]),
                    'release_date': int(parts[2]),
                    'due_date': int(parts[3]),
                    'tardcost': int(parts[4]),
                    'mpm_time': int(parts[5])
                }

            elif current_section == 'precedence':
                parts = line.split()
                job_id = int(parts[0])
                num_modes = int(parts[1])
                n_successors = int(parts[2])
                successors = list(map(int, parts[3:]))
                data['precedence'][job_id] = {
                    'modes': num_modes,
                    'n_successors': n_successors,
                    'successors': successors
                }

            elif current_section == 'duration_resources':
                parts = line.split()
                job_id = int(parts[0])
                mode = int(parts[1])
                duration = int(parts[2])
                resources = list(map(int, parts[3:]))
                data['duration_resources'][job_id] = {
                    'mode': mode,
                    'duration': duration,
                    'resources': resources
                }

            elif current_section == 'resource_availability':
                parts = line.split()
                resource = parts[0]
                quantity = int(parts[1])
                data['resource_availability'][resource] = {
                    'quantity': quantity
                }

    return data
