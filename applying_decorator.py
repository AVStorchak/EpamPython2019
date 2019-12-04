def applydecorator(initial_func):
    def intermediate_decorator(f):
        def core_decorator(*args, **kwargs):
            result = initial_func(f, *args, **kwargs)
            return result
        return core_decorator
    return intermediate_decorator
