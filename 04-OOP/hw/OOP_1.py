import datetime


class Homework:
    def __init__(self, text, term):
        self.text = text
        self.created = datetime.datetime.now()
        self.deadline = datetime.timedelta(days=term)

    def is_active(self):
        current_time = datetime.datetime.now()
        return current_time <= (self.created + self.deadline)


class Student:
    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name

    def do_homework(self, task):
        if task.is_active():
            return task
        else:
            print('You are late')


class Teacher():
    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name

    def create_homework(self, text, term):
        created_homework = Homework(text, term)
        return created_homework