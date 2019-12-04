def collatz_steps(n, step_count=0):
    if not isinstance(n, (int, float)) or n%1 != 0:
        print('Please enter an integer!')
        return False
    elif n <= 0:
        print('Please enter a number that is greater than 0!')
        return False

    if n % 2 == 0:
        n = n / 2
        step_count += 1
    elif n == 1:
        return step_count
    elif n % 2 == 1:
        n = 3*n + 1
        step_count += 1

    return collatz_steps(n, step_count)
