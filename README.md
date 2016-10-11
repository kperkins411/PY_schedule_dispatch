# PY_schedule_dispatch
A python implementation of a simple round robin scheduler with blocking queue and interrupts (time slicing and IO)
It is not threaded,the interrupts are sequential at times specified in app.main.  This is a python implementation of a C++ assignment that I gave.
![My image](https://github.com/kperkins411/PY_schedule_dispatch/blob/master/queues.jpg)

Joblist uses File_IO to load a list of jobs from the default jobs file (defined in constants.DEFAULT_PCB_FILE)
The file consists of rows of 4 numbers like so
  2,5,4 ,0
  3,3,10,1
  5,15,12,1
The 1st=process_number, 2nd=start_time, 3rd = cpu_time, 4th = io_time
The 3rd means how many ticks the process should run before its finished with cpu calcs.
The 4th just means there is 1 IO operation after the cpu_time is up, if 1 when cpu_time is
done the process is moved to a blocke queue (blockedQ) waiting for the next IO_interrupt, when that 
happens all processes on the blocked queue are moved to the readyQ
