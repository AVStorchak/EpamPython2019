import functools


euler_9 = [[a, b, (1000-a-b)] for b in range(1, 500) for a in range(1, 333) if a**2+b**2 == (1000-a-b)**2][0]

euler_6 = sum([b for b in range(101)])**2 - sum([b**2 for b in range(101)])

euler_48 = sum([i**i for i in range(1, 1001)]) % (10**10)

euler_40 = functools.reduce((lambda x, y: int(x) * int(y)), ["".join([str(i) for i in range(1000000)])[10**pos] for pos in range(7)])

print(euler_9, euler_6, euler_48, euler_40, sep = "\n")