import sched
import time
import os

scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name):
    print("EVENT:", time.time(), name)
    os.system("python download_data.py")
	
for x in range(0, 5):
    scheduler.enter(60 * x, 1, print_event, (x,))

print("START:", time.time())

scheduler.run()

