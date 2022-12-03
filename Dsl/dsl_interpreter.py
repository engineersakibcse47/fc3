# Use this interpreter, by typing 'python dsl_interpreter.py habits_tracker.dsl' into the console.
# If you want to use some other .dsl file, just change the path :)

import sys

# my functions:
# (could be outsourced in its own module)

functions = {'minuites': lambda a, b: a + round((b/60),2),
             'hours': lambda a, b: a + b}

variables = {}

# check if exactly two files are given (interpreter + dsl)
if len(sys.argv) != 2:
    sys.exit(1)

# open .dsl and check each line
with open(sys.argv[1]) as file:
    # initialization for actual routine situation
    routine = {"Exercise": 0,
               "Prayer": 0,
               "Read_News": 0,
               "Walk": 0,
               "Homework": 0,
               "Cycleing": 0,
               "Study": 0,
               "Refreshment": 0               
               }

    for line in file:
        line = line.strip()

        # check if the line is a comment
        if not line or line[0] == '~':
            continue
        parts = line.split()
        #print("parts: " + parts[0])

        # check the instructions for each line and execute them
        if parts[0] == 'How':
            print("Your spent time:" + str(routine[parts[2]]) + " hrs " + parts[2] + " this week ")

        else:
            a = routine[parts[1]]
            b = int(parts[0])

            routine[parts[1]] = functions[parts[2]](a, b)