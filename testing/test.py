import multiprocessing
import time
import os
import signal

def foo(stop_event):
    while not stop_event.is_set():
        print("processing running")
        time.sleep(1)
    print("STOPPED")

stop_event = multiprocessing.Event()

p = multiprocessing.Process(target=foo, args=(stop_event,))
p.start()

time.sleep(3)

stop_event.set()
p.join()
