def is_armstrong(number):
    import functools

    digit_list = [int(i) for i in str(number)]
    armstrong_sum = functools.reduce((lambda x, y: x+y),
                    map(lambda x: x**(len(digit_list)), digit_list))

    return number == armstrong_sum
