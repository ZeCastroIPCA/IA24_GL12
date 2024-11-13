# Import contraint lybrary
from constraint import *
# Import parse_file function from parse_file.py
from parse_file import parse_file

# Read the file
file_path = './dataset.txt'
parsed_data = parse_file(file_path)

# Extract the data from the parsed file
projects_data = parsed_data['projects']
precedence_data = parsed_data['precedence']
duration_resources_data = parsed_data['duration_resources']
resource_availability_data = parsed_data['resource_availability']

# Print the data
# print("Projects: ", projects_data)
# print("Precedence: ", precedence_data)
# print("Duration & Resources: ", duration_resources_data)
# print("Resource Availability: ", resource_availability_data)

# Create a dictionary to store the project variables
jobs = {}
resources = {}
for project in projects_data:
    # print(f"Project: {project}")
    for job, job_data in precedence_data.items():
        # print(f"\nJob: {job}")
        # print(f"Succesors: {job_data['successors']}")
        # print(f"Duration: {duration_resources_data[job]['duration']}")
        # print(f"Resources: {duration_resources_data[job]['resources']}")

        # Store the job data in the jobs dictionary
        jobs[job] = {
            'successors': job_data['successors'],
            'duration': duration_resources_data[job]['duration'],
            'resources': duration_resources_data[job]['resources']
        }

    # Store the resources availability
    for resource in resource_availability_data.keys():
        resources[resource] = resource_availability_data[resource]['quantity']


# Print the jobs and resources
print(f"\nJobs: {jobs}")
print(f"\nResources: {resources}")
# Start the CSP problem
problem = Problem()
