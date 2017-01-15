"""
code pieces demonstrating how to solve the problems of shared state
translated course note: https://github.com/wizardforcel/sicp-py-zh/blob/master/ch4.md
"""

from threading import Lock


# Using Lock
def make_withdraw(balance):
    balance_lock = Lock()

    def withdraw(amount):
        nonlocal balance
        # try to acquire the lock
        balance_lock.acquire()
        # once successful, enter the critical section
        if amount > balance:
            print("Insufficient funds")
        else:
            balance -= amount
            print(balance)
        # upon exiting the critical section, release the lock
        balance_lock.release()

    return withdraw


"""
demo of 2 processes

>>> w = make_withdraw(10)
>>> w(8)
>>> w(7)

P1                                  P2
acquire balance_lock: ok
read balance: 10                    acquire balance_lock: wait
read amount: 8                      wait
8 > 10: False                       wait
if False                            wait
10 - 8: 2                           wait
write balance -> 2                  wait
read balance: 2                     wait
print 2                             wait
release balance_lock                wait
                                    acquire balance_lock:ok
                                    read balance: 2
                                    read amount: 7
                                    7 > 2: True
                                    if True
                                    print 'Insufficient funds'
                                    release balance_lock
"""

# Using Semaphore
from threading import Semaphore

db_semaphore = Semaphore(2)
database = []


def insert(data):
    db_semaphore.acquire()
    database.append(data)
    db_semaphore.release()


"""
demo of 3 processes

>>> insert(7)
>>> insert(8)
>>> insert(9)

P1                          P2                           P3
acquire db_semaphore: ok    acquire db_semaphore: wait   acquire db_semaphore: ok
read data: 7                wait                         read data: 9
append 7 to database        wait                         append 9 to database
release db_semaphore: ok    acquire db_semaphore: ok     release db_semaphore: ok
                            read data: 8
                            append 8 to database
                            release db_semaphore: ok
"""

# Conditional variables (pseudo code)
from threading import Condition

step1_finished = 0
start_step2 = Condition()
B = [2, 0]
C = [0, 5]
A = [0, 0]
M = [[1, 2], [1, 2]]
V = [0, 0]


def do_step_1(index):
    global step1_finished, start_step2, A, B, C
    A[index] = B[index] + C[index]
    # access the shared state that determines the condition status
    start_step2.acquire()
    step1_finished += 1
    if step1_finished == 2:  # if the condition is met
        start_step2.notifyAll()  # send the signal
    # release access to shared state
    start_step2.release()


def do_step_2(index):
    # wait for the condition
    global start_step2, V, M, A
    start_step2.wait()
    V[index] = M[index] * A


"""
demo of conditional variable

>>> do_step_1(0)
>>> do_step_1(1)
>>> do_step_2(0)
>>> do_step_2(1)

P1                            P2
read B1: 2
read C1: 0
calculate 2+0: 2
write 2 -> A1                 read B2: 0
acquire start_step2: ok       read C2: 5
write 1 -> step1_finished     calculate 5+0: 5
step1_finished == 2: false    write 5-> A2
release start_step2: ok       acquire start_step2: ok
start_step2: wait             write 2-> step1_finished
wait                          step1_finished == 2: true
wait                          notifyAll start_step_2: ok
start_step2: ok               start_step2:ok
read M1: (1 2)                read M2: (1 2)
read A:(2 5)
calculate (1 2). (2 5): 12    read A:(2 5)
write 12->V1                  calculate (1 2). (2 5): 12
                              write 12->V2
"""

# Dead Lock (2 processes locking each other's variable while waiting for the other to release some variable)

x_lock = Lock()
y_lock = Lock()
x = 1
y = 0


def compute():
    global x, y
    x_lock.acquire()
    y_lock.acquire()
    y = x + y
    x = x * x
    y_lock.release()
    x_lock.release()


def anti_compute():
    global x, y
    y_lock.acquire()
    x_lock.acquire()
    y -= x
    x *= 3
    x_lock.release()
    y_lock.release()


"""
demo of dead lock

dead lock happens if compute() and anti_compute() are executed in parallel,
and happen to interleave with each other as follows:

>>> compute()
>>> anti_compute()

P1                          P2
acquire x_lock: ok          acquire y_lock: ok
acquire y_lock: wait        acquire x_lock: wait
wait                        wait
wait                        wait
wait                        wait
...                         ...
"""
