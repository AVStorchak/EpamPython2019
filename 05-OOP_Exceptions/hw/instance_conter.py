def instances_counter(cls):
    instance_count = 0

    class New_cls(cls):
        def __init__(self):
            nonlocal instance_count
            instance_count += 1

        @classmethod
        def get_created_instances(cls):
            nonlocal instance_count
            print(instance_count)

        @classmethod
        def reset_instances_counter(cls):
            nonlocal instance_count
            print(instance_count)
            instance_count = 0

    return New_cls


@instances_counter
class User:
    pass


if __name__ == '__main__':

    User.get_created_instances()  # 0
    user, _, _ = User(), User(), User()
    user.get_created_instances()  # 3
    user.reset_instances_counter()  # 3