class Suppressor:
    def __init__(self, *args, **kwargs):
        self.errors = args

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        return exc_type in self.errors or issubclass(exc_type, (self.errors))
