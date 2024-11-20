# CSP Solver
This is a simple CSP solver that uses backtracking to solve CSP problems. The solver is implemented in Python.
## Features
### Supported files
This is an example of a supported file. The file should contain the following sections:
```txt
************************************************************************
#General Information
************************************************************************
#Projects summary
pronr. 	#jobs 	rel.date 	duedate 	tardcost 	MPM-Time
 1      8      0         11        0         11
************************************************************************
#Precedence relations
#jobnr.    #modes  #successors   successors
   1        1          2           2   3
   2        1          1           4
   3        1          1           4
   4        1          0
   5        1          2          2   3
   6        1          1          4
   7        1          1          4
   8        1          0
************************************************************************
#Duration and resources
#jobnr. mode duration   R1   R2
  1      1     2       1    0
  2      1     3       0    1
  3      1     4       0    1
  4      1     1       0    1
  5      1     2       1    0
  6      1     3       0    1
  7      1     4       0    1
  8      1     1       0    1
************************************************************************
#Resource availability
#resource   qty
R1      1   
R2      2
************************************************************************
```
## How to replicate
### Install dependencies (contraint library)
```bash
pip3 install python-constraint
```
### Run the solver
```bash
python3 csp.py
```
## Output
### Example output
The output will be a list of jobs with their respective start and end times.
```txt
==================================================
SOLUTION FOUND!
==================================================

Total makespan: 20 time units

Detailed Schedule:
--------------------------------------------------
Job        Start      Duration   End       
--------------------------------------------------
5          11         2          13        
7          12         4          16        
6          12         3          15        
1          13         2          15        
3          15         4          19        
2          16         3          19        
4          19         1          20        
8          19         1          20        

Resource Utilization:
--------------------------------------------------
Maximum resource utilization:
R1: 1/1 units (max/capacity)
R2: 2/2 units (max/capacity)

==================================================
```