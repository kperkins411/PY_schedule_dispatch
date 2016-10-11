# PY_schedule_dispatch
A python implementation of a simple round robin scheduler with blocking queue and interrupts (time slicing and IO).
It is not threaded,the interrupts are sequential at times specified in app.main.  This is a python implementation of a C++ assignment that I gave.
Here is the [assignment](https://github.com/kperkins411/PY_schedule_dispatch/blob/master/410_P2.pdf) which contains a detailed description of all the bits.<br>
Jobs to run are stored in a file that consists of rows with 4 numbers each, like so<BR>
  2,5,4 ,0 <br>
  3,3,10,1 <br>
  5,15,12,1<br>
The 1st=process_number, 2nd=start_time, 3rd = cpu_time, 4th = io_time

These jobs are managed by JobList and parceled out to the Dispatcher whenever they are supposed to start.  
The dispatcher manages the ready and blocked queues and the current processor job. 
Together it all simulates the following system:<br><br>
![My image](https://github.com/kperkins411/PY_schedule_dispatch/blob/master/queues.jpg)

And generates a plot showing how each process would be scheduled on a single CPU<br><br>
![My image](https://github.com/kperkins411/PY_schedule_dispatch/blob/master/scatterplot.jpg)

