from abc import ABC, abstractmethod
import yaml


class AbstractStarter(ABC):
    @abstractmethod
    def prepare(self):
        pass


class ConcreteVegStarter(AbstractStarter):
    def prepare(self, menu):
        result = menu['first_courses']['vegan']
        return result


class ConcreteChildStarter(AbstractStarter):
    def prepare(self, menu):
        result = menu['first_courses']['child']
        return result


class ConcreteChineseStarter(AbstractStarter):
    def prepare(self, menu):
        result = menu['first_courses']['chinese']
        return result


class AbstractSecondCourse(ABC):
    @abstractmethod
    def prepare(self):
        pass


class ConcreteVegSecondCourse(AbstractSecondCourse):
    def prepare(self, menu):
        result = menu['second_courses']['vegan']
        return result


class ConcreteChildSecondCourse(AbstractSecondCourse):
    def prepare(self, menu):
        result = menu['second_courses']['child']
        return result


class ConcreteChineseSecondCourse(AbstractSecondCourse):
    def prepare(self, menu):
        result = menu['second_courses']['chinese']
        return result


class AbstractDrink(ABC):
    @abstractmethod
    def prepare(self):
        pass


class ConcreteVegDrink(AbstractDrink):
    def prepare(self, menu):
        result = menu['drinks']['vegan']
        return result


class ConcreteChildDrink(AbstractDrink):
    def prepare(self, menu):
        result = menu['drinks']['child']
        return result


class ConcreteChineseDrink(AbstractDrink):
    def prepare(self, menu):
        result = menu['drinks']['chinese']
        return result


class AbstractMeal(ABC):
    @abstractmethod
    def get_starter(self, collaborator: AbstractStarter):
        pass

    @abstractmethod
    def get_second_course(self, collaborator: AbstractSecondCourse):
        pass

    @abstractmethod
    def get_drink(self, collaborator: AbstractDrink):
        pass

    @abstractmethod
    def serve(self):
        pass


class AbstractFactory(ABC):
    @abstractmethod
    def get_starter(self):
        pass

    @abstractmethod
    def get_second_course(self):
        pass

    @abstractmethod
    def get_drink(self):
        pass


class ConcreteFactoryVeg(AbstractFactory):
    def get_starter(self, menu):
        starter = ConcreteVegStarter()
        return starter.prepare(menu)

    def get_second_course(self, menu):
        second_course = ConcreteVegSecondCourse()
        return second_course.prepare(menu)

    def get_drink(self, menu):
        drink = ConcreteVegDrink()
        return drink.prepare(menu)


class ConcreteFactoryChild(AbstractFactory):
    def get_starter(self, menu):
        starter = ConcreteChildStarter()
        return starter.prepare(menu)

    def get_second_course(self, menu):
        second_course = ConcreteChildSecondCourse()
        return second_course.prepare(menu)

    def get_drink(self, menu):
        drink = ConcreteChildDrink()
        return drink.prepare(menu)


class ConcreteFactoryChinese(AbstractFactory):
    def get_starter(self, menu):
        starter = ConcreteChineseStarter()
        return starter.prepare(menu)

    def get_second_course(self, menu):
        second_course = ConcreteChineseSecondCourse()
        return second_course.prepare(menu)

    def get_drink(self, menu):
        drink = ConcreteChineseDrink()
        return drink.prepare(menu)


def client_code(factory):
    with open("menu.yml", 'r', encoding='utf-8') as stream:
        try:
            menu = (yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)

    meals = menu["Friday"]
    starter = factory.get_starter(meals)
    second_course = factory.get_second_course(meals)
    drink = factory.get_drink(meals)
    print(f"The meal includes:\n - {starter}\n - {second_course}\n - {drink}")


if __name__ == "__main__":
    print("Chinese menu for Friday:")
    client_code(ConcreteFactoryChinese())
    print("Child menu for Friday:")
    client_code(ConcreteFactoryChild())
    print("Vegetarian menu for Friday:")
    client_code(ConcreteFactoryVeg())
