def is_permutation(a, b):
    if len(a) != len(b):
        return False

    dict_a = {}
    dict_b = {}

    for char in a:
        dict_a[char] = 1 + dict_a.get(char, 0)

    for char in b:
        dict_b[char] = 1 + dict_b.get(char, 0)

    return dict_a == dict_b