# PY_schedule_dispatch
A python implementation of a simple round robin scheduler with blocking queue and interrupts (time slicing and IO).
It is not threaded,the interrupts are sequential at times specified in app.main.  This is a python implementation of a C++ assignment that I gave.


Here is the [assignment](https://github.com/kperkins411/PY_schedule_dispatch/blob/master/410_P2.pdf) which contains a detailed description of all the bits.

It simulates the following system
![My image](https://github.com/kperkins411/PY_schedule_dispatch/blob/master/queues.jpg)

And generates a plot showing how each process would be scheduled on a single CPU
![My image](https://github.com/kperkins411/PY_schedule_dispatch/blob/master/scatterplot.jpg)

Jobs to run are stored in a file that consists of rows with 4 numbers each, like so
  2,5,4 ,0
  3,3,10,1
  5,15,12,1
The 1st=process_number, 2nd=start_time, 3rd = cpu_time, 4th = io_time

These jobs are managed by JobList and parceled out to the Dispatcher whenever they are supposed to start.  
The dispatcher manages the queue of ready jobs, the queue of blocked jobs and the currently running job.  
App.main contains a loop that progresses i tickcount per iteration. It;  
  invokes JobLists do_tick() to see if any jobs are available this tick to load into the dispatcher
  invokes Dispatcher.do_tick() to manage moving processes around on the queues and currently running process
  handles invoking timeslice interrupts
  handles invoking io_interrupts
  generates a list (results.txt) of what process is running at what tick
Plotprocess will plot the results on a nice chart to see whats happenning when.

Here is a plot of what the running processes look like






