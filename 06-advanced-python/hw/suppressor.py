class Suppressor:
    def __init__(self, *args, **kwargs):
        self.errors = args

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type in self.errors:
            return True
