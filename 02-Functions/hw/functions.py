def letters_range(*args, **kwargs):
    if len(args) == 1:
        stop = args[0]
        start = 'a'
        step = 1
    elif len(args) == 2:
        start, stop = args
        step = 1
    elif len(args) == 3:
        start, stop, step = args

    out = [chr(i) for i in range(ord(start), ord(stop), step)]

    if len(kwargs) > 0:
        for pos, char in enumerate(out):
            if char in kwargs:
                out[pos] = kwargs[char]

    return out


def make_it_count(func, counter_name):
    def func_amended(*args, **kwargs):
        try:
            globals()[counter_name] += 1
        except KeyError:
            print("The counter variable name must be passed as a string")
        result = func(*args, **kwargs)
        return result
    return func_amended


def atom(value=None):
    atom_value = value

    def get_value():
        nonlocal atom_value
        print(atom_value)

    def set_value(new_value):
        nonlocal atom_value
        atom_value = new_value
        print(atom_value)

    def process_value(*args):
        nonlocal atom_value
        for func in args:
            try:
                atom_value = func(atom_value)
            except TypeError:
                atom_value = func()
        print("Final value:", atom_value)

    def delete_value():
        nonlocal atom_value
        atom_value = None

    return(get_value, set_value, process_value, delete_value)


def modified_func(func, *fixated_args, **fixated_kwargs):
    import inspect
    from inspect import signature, Parameter

    def new_func(*args, **kwargs):
        nonlocal fixated_args
        nonlocal fixated_kwargs

        working_args = fixated_args
        working_kwargs = fixated_kwargs

        for i in args:
            working_args += (i,)

        working_kwargs.update(kwargs)
        result = func(*working_args, **working_kwargs)

        return result

    named_arg_list = []
    positional_arg_list = []
    named_args = {}
    position = 0

    try:
        for x, p in signature(func).parameters.items():
            if p.default != Parameter.empty and x not in inspect.getfullargspec(func).kwonlyargs:
                named_arg_list.append(x)
            elif p.default == Parameter.empty and x not in inspect.getfullargspec(func).kwonlyargs:
                positional_arg_list.append(x)
            elif x == 'args':
                break

        if len(fixated_args) > len(positional_arg_list):
            tail_args = fixated_args[(len(positional_arg_list)):]
        else:
            tail_args = []

        for arg in named_arg_list[:len(tail_args)]:
            if arg not in fixated_kwargs:
                named_args[arg] = tail_args[position]
                position += 1

    except ValueError:
        named_args = 'A built-in function, no named arguments were passed as positional ones.'

    try:
        source_code = inspect.getsource(func)
    except TypeError:
        source_code = 'Source is not available, possibly a C module.'

    new_func.__name__ = f'func_{func.__name__}'

    new_func.__doc__ = f"""A func implementation of {func.__name__} with pre-applied arguments being:
                        <{fixated_args}
                        {fixated_kwargs}
                        while the following named arguments were passed
                        as positional ones with the following values:
                        {named_args}
                        >
                        Source code:
                        {source_code}"""

    return new_func