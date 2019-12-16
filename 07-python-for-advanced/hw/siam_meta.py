class SiamMeta(type):

    def __new__(mcls, name, bases, attrs):
        _instances = {}
        cls = super(SiamMeta, mcls).__new__(mcls, name, bases, attrs)
        cls._instances = _instances

        return cls

    def __call__(cls, *args, **kwargs):
        import weakref

        def reach_other_instance(*args, **kwargs):
            processed_kwargs = [i[1] for i in sorted(kwargs.items(),
                                key=lambda item: item[0])]
            address = list(args) + processed_kwargs
            try:
                for var, combo in cls._instances.items():
                    if combo == address:
                        other_instance = var
                return other_instance()
            except UnboundLocalError:
                print('There is no such instance!')

        def delete_instance(instance):
            try:
                del cls._instances[(weakref.ref(instance))]
            except NameError:
                print('There is no such instance!')

        processed_kwargs = [i[1] for i in sorted(kwargs.items(),
                            key=lambda item: item[0])]
        arg_kwarg_combo = list(args) + processed_kwargs

        if arg_kwarg_combo not in cls._instances.values():
            instance = super(SiamMeta, cls).__call__(*args, **kwargs)
            cls._instances[weakref.ref(instance)] = arg_kwarg_combo
            cls.__del__ = delete_instance
            instance.connect = reach_other_instance
            instance.pool = cls._instances
        else:
            for var, combo in cls._instances.items():
                if combo == arg_kwarg_combo:
                    instance = var()
        return instance


class SiamObj(metaclass=SiamMeta):
    def __init__(self, *args, **kwargs):
        self.__dict__ = dict(kwargs)
        self.args = args
        self.kwargs = kwargs
