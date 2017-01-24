# threading
# multiple threads exist within a single interpreter
# due to GIL, the interpreter only interprets code in one thread at a time, while I/O may run in parallel
import threading
import multiprocessing
from time import sleep


def thread_hello():
    """running the same function thread_say_hello with 2 different threads, prints can happen in any order"""
    other = threading.Thread(target=thread_say_hello, args=())
    other.start()
    thread_say_hello()


def thread_say_hello():
    print('hello from', threading.current_thread().name)


# multiprocessing
# each interpreter run within a separate process, and the processes do not generally share data
def process_hello():
    """analogous to those in threading"""
    other = multiprocessing.Process(target=process_say_hello, args=())
    other.start()
    process_say_hello()


def process_say_hello():
    print('hello from', multiprocessing.current_process().name)


# the problem of shared state, "race condition"
counter = [0]


def increment():
    count = counter[0]
    """
    switch thread during a sequence of atomic operations of incrementing
    so that counter[0] is accessed concurrently, producing unexpected result sometimes
    """
    sleep(0)  # the interpreter often does switch at the sleep call
    counter[0] = count + 1


other = threading.Thread(target=increment, args=())
other.start()
increment()
print('count is now: ', counter[0])

# using synchronized data structure (queue)
"""
We have marked the consumer thread as a daemon, which means that the program will not wait for
that thread to complete before exiting. This allows us to use an infinite loop in the consumer.
However, we do need to ensure that the main thread exits, but only after all items have been
consumed from the Queue. The consumer calls the task_done method to inform the Queue that it is
done processing an item, and the main thread calls the join method, which waits until all items
have been processed, ensuring that the program exits only after that is the case.
"""
from queue import Queue

queue = Queue()


def synchronized_consume():
    while True:
        sleep(3)
        print('got an item:', queue.get())
        """
        task_done decrements a counter (incremented by "put").
        when the counter reaches 0, the "queue.join()" call is unblocked
        """
        queue.task_done()


def synchronized_produce():
    consumer = threading.Thread(target=synchronized_consume, args=())
    """
    Mark the worker thread as a daemon so that we don't wait for it to complete before exiting.
    If the worker threads are non-daemon, their continuing execution prevents the program
    from stopping irrespective of whether the main thread has finished
    """
    consumer.daemon = True
    consumer.start()
    for i in range(10):
        queue.put(i)
    """
    queue.join() blocks the main thread until the workers have processed everything in the queue,
    however it doesn't block the worker threads, which continue executing the infinite loops
    """
    queue.join()


synchronized_produce()

# locks
seen = set()
seen_lock = threading.Lock()


def already_seen(item):
    with seen_lock:
        if item not in seen:
            seen.add(item)
            return False
        return True


# barriers
counters = [0, 0]
barrier = threading.Barrier(2)


def count(thread_num, steps):
    for _ in range(steps):
        other = counters[1 - thread_num]
        barrier.wait()  # wait for reading complete
        counters[thread_num] = other + 1
        barrier.wait()  # wait for writing complete


def threaded_count(steps):
    other = threading.Thread(target=count, args=(1, steps))
    other.start()
    count(0, steps)
    print('counters:', counters)


threaded_count(10)


# message passing through Pipe between processes
def process_consume(in_pipe):
    while True:
        item = in_pipe.recv()
        if item is None:
            return
        print('got an item:', item)


def process_produce():
    pipe = multiprocessing.Pipe(False)
    consumer = multiprocessing.Process(target=process_consume, args=(pipe[0],))
    consumer.start()
    for i in range(10):
        pipe[1].send(i)
    pipe[1].send(None)  # done signal


process_produce()


# deadlock on processes
def deadlock(in_pipe, out_pipe):
    item = in_pipe.recv()
    print('got an item:', item)
    out_pipe.send(item + 1)


def create_deadlock():
    """
    recv method blocks until an item is available. Since neither process has sent anything,
    both will wait indefinitely for the other to send it data, resulting in deadlock.
    """
    pipe = multiprocessing.Pipe()
    other = multiprocessing.Process(target=deadlock, args=(pipe[0], pipe[1]))
    other.start()
    deadlock(pipe[1], pipe[0])


create_deadlock()