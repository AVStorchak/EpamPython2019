def measure_it(counter_var):
    def intermediate_func(original_function):
        is_measured = False

        def measured_function(*args, **kwargs):
            import time
            nonlocal is_measured

            if is_measured:
                return original_function(*args, **kwargs)
            else:
                start_time = time.time()
                is_measured = True
                result = original_function(*args, **kwargs)

                is_measured = False
                end_time = time.time()
                duration = end_time - start_time
                globals()[counter_var]['duration'] += duration
                globals()[counter_var]['count'] += 1
                return result
        return measured_function
    return intermediate_func


@measure_it('fib1_count')
def fibonacci_1(n):
    """Recursive calculation"""
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_1(n-1) + fibonacci_1(n-2)


@measure_it('fib2_count')
def fibonacci_2(n, table=[]):
    """Dynamic programming calculation"""
    while len(table) < n+1:
        table.append(0)

    if n <= 1:
        return n
    else:
        if table[n-1] == 0:
            table[n-1] = fibonacci_2(n-1)

        if table[n-2] == 0:
            table[n-2] = fibonacci_2(n-2)

        table[n] = table[n-2] + table[n-1]
    return table[n]


@measure_it('fib3_count')
def fibonacci_3(n):
    """Space optimization calculation"""
    a = 0
    b = 1
    if n == 0:
        return a
    elif n == 1:
        return b
    else:
        for i in range(2, n+1):
            c = a + b
            a = b
            b = c
        return b


@measure_it('fib4_count')
def fibonacci_4(n):
    """Memoization calculation"""
    if n in fib4_storage:
        return fib4_storage[n]

    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        result = fibonacci_4(n-1) + fibonacci_4(n-2)
        fib4_storage[n] = result
        return result


fib4_storage = {}
fib1_count = {'count': 0, 'duration': 0}
fib2_count = {'count': 0, 'duration': 0}
fib3_count = {'count': 0, 'duration': 0}
fib4_count = {'count': 0, 'duration': 0}

for n in range (35):
    fibonacci_1(n)

for n in range (10000):
    fibonacci_2(n)
    fibonacci_3(n)
    fibonacci_4(n)

print(fib1_count, fib2_count, fib3_count, fib4_count, sep='\n')

"""
for n from 0 to 9999 (from 0 to 34 for Recursive calculation):
Recursive calculation:           {'count': 35, 'duration': 32.23584342002869} - worst result
Dynamic programming calculation: {'count': 10000, 'duration': 0.022001981735229492} - best result
Space optimization calculation:  {'count': 10000, 'duration': 12.613720655441284}
Memoization calculation:         {'count': 10000, 'duration': 0.03900337219238281}
"""
