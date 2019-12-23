class Component:
    def get_cost(self):
        raise NotImplementedError("Override get_cost method")


class BaseCoffee(Component):
    def get_cost(self):
        return 90


class AbstractCoffeeIngredient(Component):
    def __init__(self, decorated_coffee):
        self.decorated_coffee = decorated_coffee

    def get_cost(self):
        return self.decorated_coffee.get_cost()


class Whip(AbstractCoffeeIngredient):
    def __init__(self, decorated_coffee):
        super(Whip, self).__init__(decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost() + 15


class Marshmallow(AbstractCoffeeIngredient):
    def __init__(self, decorated_coffee):
        super(Marshmallow, self).__init__(decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost() + 35


class Syrup(AbstractCoffeeIngredient):
    def __init__(self, decorated_coffee):
        super(Syrup, self).__init__(decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost() + 20


if __name__ == "__main__":
    coffee = BaseCoffee()
    coffee = Whip(coffee)
    coffee = Marshmallow(coffee)
    coffee = Syrup(coffee)
    print("Итоговая стоимость за кофе: {}".format(str(coffee.get_cost())))
