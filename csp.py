# Import contraint lybrary
from constraint import *
# Import parse_file function from parse_file.py
from parse_file import parse_file

# Read the file
file_path = './dataset.txt'  # Replace with your actual file path
parsed_data = parse_file(file_path)

projects_data = parsed_data['projects']
precedence_data = parsed_data['precedence']
duration_resources_data = parsed_data['duration_resources']
resource_availability_data = parsed_data['resource_availability']

# Print the data
print("Projects: ", projects_data)
print("Precedence: ", precedence_data)
print("Duration & Resources: ", duration_resources_data)
print("Resource Availability: ", resource_availability_data)
