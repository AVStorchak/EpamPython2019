import datetime
from collections import defaultdict


class DeadlineError(Exception):
    '''You are late'''


class Homework:
    def __init__(self, text, term):
        self.text = text
        self.created = datetime.datetime.now()
        self.deadline = datetime.timedelta(days=term)

    def is_active(self):
        current_time = datetime.datetime.now()
        return current_time <= (self.created + self.deadline)


class HomeworkResult:
    def __init__(self, author, task, solution):
        if not isinstance(task, Homework):
            raise TypeError('You gave a not Homework object')
        self.homework = task
        self.solution = solution
        self.author = author
        self.created = datetime.datetime.now()


class Person:
    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name


class Student(Person):
    def do_homework(self, task, solution):
        result = HomeworkResult(self, task, solution)
        if task.is_active():
            return result
        else:
            raise DeadlineError('You are late')


class Teacher(Person):
    homework_done = defaultdict(set)

    @staticmethod
    def create_homework(text, term):
        created_homework = Homework(text, term)
        return created_homework

    @classmethod
    def check_homework(cls, hw_done):
        if len(hw_done.solution) > 5:
            cls.homework_done[hw_done.homework].add(hw_done)
            return True
        else:
            return False

    @classmethod
    def reset_results(cls, task=None):
        if task is None:
            cls.homework_done.clear()
        else:
            del cls.homework_done[task]