README: Poorwa Hirve 
COURSE: CSCI-5673 Distributed Systems

Assignment: Create a Fault Tolerant Stack Data Structure

HOW TO COMPILE AND RUN:

Setup raftos by following the README-old.md file.

Go to the examples folder and run the run_cluster.sh file which runs node.py

STATUS:

Can push, pop, top, get id, create stack. Even if 2 servers fail the others keep working.

Sources of potential errors include if some internal processing kills some of the main processes.


Edits to original raftos:

Added a replicated delete function to ReplicatedList.
