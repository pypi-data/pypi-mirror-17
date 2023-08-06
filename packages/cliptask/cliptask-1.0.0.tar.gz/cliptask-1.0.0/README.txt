
A lightweight framework for running trivially parallelisable tasks using
Python's multiprocessing module.


Introduction:
----------------
This framework is suitable for batch processing a set of inputs, where the processing involves  series of operations in a defined order. An example would be writing a data calibration pipeline (dark subtraction, flat fielding, bad pixel masking etc.), then running on it many different images. This task is trivially parallelisable, because no result depends on the results of any other image.

Python has a multiprocessing module to simply such tasks, but it's not perfect. If your pipeline crashes on any one image, you get no results for any image. It's also difficult to find out which task crashed, or how to debug it.

Clips and Tasks
----------------
Clips and tasks simplifies the result some. A clipboard is a glorified dictionary that stores inputs and outputs. A task is a function that takes a clipboard as input, modifies it, and returns a clipboard as output. This module provides a decorator to turn a function into a task. A task will check that the function returns an output, and decides whether to call the debugger if an error occurs.


Installation:
python setup.py install

or, to install locally,
python setup.py install --user


Usage
--------------
import task
#Create a configuration dictionary

cfg = task.Clipboard()

#Set debug status. In debug mode pdb is called if a task raises an exception,
#otherwise, the pipeline is halted silently.
cfg['debug'] = True

#Set a list of functions to be called by the pipeline, in the order they 
#should be called. Note, these are strings, not functions. This is because
#Python doesn't allow functions to be passed into parallel processes
cfg['taskList'] = ["func1", "func2", "func3"]

#Set some other parameters here
cfg['spam'] = 6


#Define the pipeline functions, including the task decorator
@task.task
def func1(clip):
    return clip
    
    
#Define a master function
def master(value, config):
    tasks = config['taskList']
    
    clip = task.Clipboard()
    for t in tasks:
	f = eval(t)
	clip = f(clip)
	
	
#Finally, run the master function on a range of inputs
values = range(10)
task.parmap(master, values, config)


Note:
------------
The parmap.py file is written by Sergio Oller, and licensed under the Apache License.
See code for more details. parmap's home is https://github.com/zeehio/parmap