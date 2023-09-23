# Transformation of Application Lifecycle
## Problem statement
Referring to the input file "CC Application Lifecycle.csv,”, please manipulate the file to show
Application stages as column headings and the corresponding time of stage completion as
values for each customer ID. 

Structure the output as demonstrated in the file "Application
Lifecycle Output.csv." This data wrangling endeavour is expected to be executed using the
Python programming language.

## Implementation details
### The order of the columns is not as it is in the example output
This is because I don't have any information on what the order of the columns 
should be, so the order I set is: "first come, first served". Meaning that in my 
implementation, by default, the order is set by the order in which each new column appears.
It is possible though to use the argument **header** to set the desired order (see next section)
### Arguments
All arguments are optional and can be seen by running:
```commandline
python3 t_application_lifecycle.py --help
# This should return:  
# usage: t_application_lifecycle.py [-h] in_file_name out_file_name header
#
#positional arguments:
#  in_file_name   Input file name (or full path)
#  out_file_name  Output file name (or full path)
#  header         A string representing a valid Python of a list of strings. This will force a given list of headers and therefore is only useful if we already
#                 know the columns and want to set a given order. See Readme.md for an example of how to use this argument.
#
#options:
#  -h, --help     show this help message and exit
```
To set the **header** argument, an env var can be set. An example for a Unix System would be: 
```commandline
export HEADER="['UniqueID','REGISTERED_0','ACKNOWLEDGED_0','APPROVED_0','REACKNOWLEDGED_0','CLOSED_0', 'APPOINTMENT_SCHEDULED_0','REJECTED_0','ON_HOLD_0','BLOCKED_0','TERMINATE_0','INITIATED_0', 'APPROVED_1','ON_HOLD_1','INITIATED_1','REGISTERED_1','BLOCKED_1','CLOSED_1','APPROVED_2']"
python3 t_application_lifecycle.py --header "$HEADER"
```
Please note that HEADER is a string that represents a valid Python expression of a list of strings. 
If this is not set properly, the script will fail and throw an exception.

A more complete example of how to run this script would be:
```commandline
export HEADER="['UniqueID','REGISTERED_0','ACKNOWLEDGED_0','APPROVED_0','REACKNOWLEDGED_0','CLOSED_0', 'APPOINTMENT_SCHEDULED_0','REJECTED_0','ON_HOLD_0','BLOCKED_0','TERMINATE_0','INITIATED_0', 'APPROVED_1','ON_HOLD_1','INITIATED_1','REGISTERED_1','BLOCKED_1','CLOSED_1','APPROVED_2']"
python3 t_application_lifecycle.py --header "$HEADER"
```
# Requirements
I have used **Python 3.10.12** on a laptop running **Ubuntu 22.04.3 LTS** as the OS, but this code should run in any
other Python version (higher than 3.7) or any other OS.
Other than that, the ony library used was **pytest** and that requirement is in the requirements.txt file.