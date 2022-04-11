from threading import Thread
from math import sqrt

# 定积分数值计算
def f(x: float) -> float:
    return sqrt(4 - x * x)

def integral(f, n, a, b):
    sum = 0
    dx = (b - a) / n
    x = a
    x_ = x + dx
    while(x_ <= b):
        sum += (f(x) + f(x_)) * dx / 2
        x += dx
        x_ += dx
    return sum

def parallel_integral(f, n, a, b, tn=1, tid=0):
    sum = 0
    dx = (b - a) / n
    x = a + tid * dx
    x_ = x + dx
    while(x_ <= b):
        sum += (f(x) + f(x_)) * dx / 2
        x += tn * dx
        x_ += tn * dx
    global sums
    sums += sum

N = 10000000
print(integral(f, N, 0, 2))

NUM_THREADS = 10
sums = 0
for i in range(NUM_THREADS):
    t = Thread(target=parallel_integral, args=(f, N, 0, 2, NUM_THREADS, i))
    t.run()
print(sums)
