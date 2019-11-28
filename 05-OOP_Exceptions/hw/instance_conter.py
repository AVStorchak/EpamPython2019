def instances_counter(cls):
    cls.instance_count = 0
    orig_init = cls.__init__

    def new_init(self, *args, **kwargs):
        orig_init(self, *args, **kwargs)
        cls.instance_count += 1

    @classmethod
    def get_created_instances(cls):
        print (cls.instance_count)

    @classmethod
    def reset_instances_counter(cls):
        print (cls.instance_count)
        cls.instance_count = 0

    cls.__init__ = new_init
    cls.get_created_instances = get_created_instances
    cls.reset_instances_counter = reset_instances_counter   
    return cls


@instances_counter
class User:
    pass


if __name__ == '__main__':

    User.get_created_instances()  # 0
    user, _, _ = User(), User(), User()
    user.get_created_instances()  # 3
    user.reset_instances_counter()  # 3