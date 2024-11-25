# Import constraint library
from constraint import *
# Import argument parser
import argparse
# Import custom file parsing function
from parse_file import parse_file

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("file_path")

# Parse arguments
args = parser.parse_args()
file_path = args.file_path

# Read the input file
parsed_data = parse_file(file_path)

# Extract relevant data from parsed file
projects_data = parsed_data['projects']
precedence_data = parsed_data['precedence']
duration_resources_data = parsed_data['duration_resources']
resource_availability_data = parsed_data['resource_availability']

# Create dictionaries to store project and resource information
jobs = {}
resources = {}

# Populate jobs dictionary with project information
for project in projects_data:
    for job, job_data in precedence_data.items():
        job_str = str(job)
        successors = [str(s) for s in job_data['successors']]
        
        jobs[job_str] = {
            'successors': successors,
            'duration': duration_resources_data[job]['duration'],
            'resources': duration_resources_data[job]['resources']
        }

# Populate resources dictionary with available quantities
for resource in resource_availability_data.keys():
    resources[resource] = resource_availability_data[resource]['quantity']

# Print extracted data for verification
print(f"\nJobs: {jobs}")
print(f"\nResources: {resources}")

# Calculate maximum possible timespan across all jobs
max_time = projects_data[1]['due_date']
print(f"\nMaximum Tempospan: {max_time}")

# Create CSP problem instance
problem = Problem()

# Calculate minimum possible start times based on precedence
def calculate_minimum_start_times(jobs):
    earliest_starts = {}
    for job_id in jobs:
        earliest_starts[job_id] = 1  # Default to earliest possible time
        for other_job, other_data in jobs.items():
            if job_id in other_data['successors']:
                # Ensure this job starts after the other job completes
                earliest_starts[job_id] = max(earliest_starts[job_id], 1 + jobs[other_job]['duration'])
    return earliest_starts

# Before solving, update variable domains
min_start_times = calculate_minimum_start_times(jobs)
#print(f"\nMinimum start times: {min_start_times}")
for job_id in jobs:
    problem.addVariable(job_id, range(min_start_times[job_id], max_time))

# Define precedence constraint function
def check_precedence(job1, job2):
    #print(f"Checking precedence between {job1} and {job2}")
    def constraint(time1, time2):
        # Ensure that job1 finishes before job2 starts
        return time1 + jobs[job1]['duration'] <= time2
    return constraint


# Add precedence constraints for pairs of jobs
for job_id, job_data in jobs.items():
    for successor in job_data['successors']:
        if successor in jobs:  # Ensure the successor exists
            problem.addConstraint(
                check_precedence(job_id, successor), 
                (job_id, successor)
            )

# Define resource constraint function
def check_resources(*args):
    if len(args) < len(jobs):
        return True
        
    # Get time assignments for all jobs
    assignments = dict(zip(jobs.keys(), args))
    timeline = {}
    
    # Iterate through each job
    for job_id, start_time in assignments.items():
        duration = jobs[job_id]['duration']
        job_resources = jobs[job_id]['resources']
        
        # Iterate through each time unit of the job
        for t in range(start_time, start_time + duration):
            if t not in timeline:
                timeline[t] = {r: 0 for r in resources.keys()}
            
            # Add resource usage
            for resource_idx, amount in enumerate(job_resources):
                resource = f'R{resource_idx + 1}'
                timeline[t][resource] += amount
                if timeline[t][resource] > resources[resource]:
                    return False
    return True

# Add resource constraints
problem.addConstraint(check_resources, jobs.keys())

def solve_asap(problem, jobs, resources):
    # Initial solution from the solver
    solution = problem.getSolution()
    if not solution:
        return None  # No solution found
    
    def is_feasible(solution):
        """Check if a solution is feasible with respect to constraints."""
        # Check precedence constraints
        for job_id, start_time in solution.items():
            for successor in jobs[job_id]['successors']:
                if start_time + jobs[job_id]['duration'] > solution[successor]:
                    return False

        # Check resource constraints
        timeline = {}
        for job_id, start_time in solution.items():
            duration = jobs[job_id]['duration']
            job_resources = jobs[job_id]['resources']

            for t in range(start_time, start_time + duration):
                if t not in timeline:
                    timeline[t] = {r: 0 for r in resources.keys()}

                for resource_idx, amount in enumerate(job_resources):
                    resource = f'R{resource_idx + 1}'
                    timeline[t][resource] += amount
                    if timeline[t][resource] > resources[resource]:
                        return False
        return True

    # Minimize start times iteratively
    while True:
        minimized = False
        for job_id in sorted(jobs.keys(), key=lambda j: int(j)):  # Iterate in job order
            current_start = solution[job_id]

            # Try earlier start times while maintaining feasibility
            for t in range(min_start_times[job_id], current_start):
                test_solution = solution.copy()
                test_solution[job_id] = t

                # Check feasibility
                if is_feasible(test_solution):
                    solution[job_id] = t
                    minimized = True
                    break  # Move to the next job

        if not minimized:
            break  # No further improvement possible

    return solution

# Solve the CSP problem
solution = solve_asap(problem, jobs, resources)

if solution:
    # Sort jobs by start time
    sorted_schedule = sorted(solution.items(), key=lambda x: x[1])
    
    # Calculate makespan (maximum end time)
    makespan = max(solution[job] + jobs[job]['duration'] for job in jobs)
    
    print("\n" + "="*50)
    print("SOLUTION FOUND!")
    print("="*50)
    
    print(f"\nTotal makespan: {makespan} time units")
    
    print("\nDetailed Schedule:")
    print("-"*50)
    print(f"{'Job':<10} {'Começo':<10} {'Duration':<10} {'End':<10}")
    print("-"*50)
    
    for job_id, start_time in sorted_schedule:
        duration = jobs[job_id]['duration']
        end_time = start_time + duration
        print(f"{job_id:<10} {start_time:<10} {duration:<10} {end_time:<10}")
    
    print("\nResource Utilization:")
    print("-"*50)
    
    # Calculate and display resource usage per period
    timeline = {}
    for job_id, start_time in solution.items():
        duration = jobs[job_id]['duration']
        job_resources = jobs[job_id]['resources']
        
        for t in range(start_time, start_time + duration):
            if t not in timeline:
                timeline[t] = {r: 0 for r in resources.keys()}
            
            for resource_idx, amount in enumerate(job_resources):
                resource = f'R{resource_idx + 1}'
                timeline[t][resource] += amount
    
    # Display maximum resource utilization
    print("Maximum resource utilization:")
    for resource in resources:
        max_usage = max(timeline[t][resource] for t in timeline)
        capacity = resources[resource]
        print(f"{resource}: {max_usage}/{capacity} units (max/capacity)")
    
else:
    print("\nNO SOLUTION FOUND!")
    print("The problem might be over-constrained or need more time to solve.")

print("\n" + "="*50)

# Visualize the data in a Gantt chart
import matplotlib.pyplot as plt
import pandas as pd 

# Create a DataFrame for Gantt chart
gantt_data = []
for job_id, start_time in solution.items():
    duration = jobs[job_id]['duration']
    end_time = start_time + duration
    gantt_data.append({
        'Job': job_id,
        'Começo': start_time,
        'Termina': end_time
    })

# Create a DataFrame for resource utilization
resource_data = []
for t, resources in timeline.items():
    resource_data.append({
        'Tempo': t,
        **resources
    })

# Create Gantt chart
df = pd.DataFrame(gantt_data)
fig, ax = plt.subplots(figsize=(10, 5))

# Plot Gantt chart
for i, task in enumerate(df['Job']):
    ax.plot(
        (df['Começo'][i], df['Termina'][i]),
        (i, i),
        color='b', linewidth=10
    )

# Set labels
ax.set_yticks(range(len(df['Job'])))
ax.set_yticklabels(df['Job'])
ax.set_xlabel('Tempo')
ax.set_ylabel('Job')
ax.set_title('Escala do Projeto')

# Display Gantt chart
plt.show()