import sched
import time
import os

scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name):
    print("EVENT:", time.time(), name)
    os.system("python download_data.py")

print("START:", time.time())
scheduler.enter(5, 1, print_event, ('first',))
scheduler.enter(65, 1, print_event, ('second',))
scheduler.enter(125, 1, print_event, ('third',))

scheduler.run()

