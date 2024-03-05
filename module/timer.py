#!/usr/bin/env python3

import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        rv = func()
        total = time.time() - start
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds % 1) * 1000)
        microseconds = int((seconds % 1) * 1e6)
        nanoseconds = int((seconds % 1) * 1e9)

        print(f"Time: {int(hours)} hrs {int(minutes)} min {int(seconds)} sec {milliseconds} ms {microseconds} µs {nanoseconds} ns")
        return rv
    return wrapper

@timer
def test():
    pass

test()
