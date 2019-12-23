from abc import ABC, abstractmethod


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):
    _next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class Fridge:
    def __init__(self, eggs=0, flour=0, milk=0, sugar=0, oil=0, butter=0):
        self._eggs = eggs
        self._flour = flour
        self._milk = milk
        self._sugar = sugar
        self._oil = oil
        self._butter = butter


class EggHandler(AbstractHandler):
    def handle(self, fridge):
        if fridge._eggs < min_egg_qty:
            eggs_required = min_egg_qty - fridge._eggs
            if eggs_required == 1:
                print(f"Требуется одно яйцо")
            else:
                print(f"Требуются яйца в количестве {eggs_required} шт.")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class FlourHandler(AbstractHandler):
    def handle(self, fridge):
        if fridge._flour < min_flour_amnt:
            flour_required = min_flour_amnt - fridge._flour
            print(f"Требуется мука в количестве {flour_required} г")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class MilkHandler(AbstractHandler):
    def handle(self, fridge):
        if fridge._milk < min_milk_vol:
            milk_required = min_milk_vol - fridge._milk
            print(f"Требуется молоко в объёме {milk_required} мл")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class SugarHandler(AbstractHandler):
    def handle(self, fridge):
        if fridge._sugar < min_sugar_amnt:
            sugar_required = min_sugar_amnt - fridge._sugar
            print(f"Требуется сахар в количестве {sugar_required} г")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class OilHandler(AbstractHandler):
    def handle(self, fridge):
        if fridge._oil < min_oil_qty:
            oil_required = min_oil_qty - fridge._oil
            print(f"Требуется подсолнечное масло в объёме {oil_required} мл")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class ButterHandler(AbstractHandler):
    def handle(self, fridge):
        if fridge._butter < min_butter_amnt:
            butter_required = min_butter_amnt - fridge._butter
            print(f"Требуется сливочное масло в количестве {butter_required} г")
        if self._next_handler:
            return self._next_handler.handle(fridge)


def check_fridge(fridge):
    egg_handler = EggHandler()
    flour_handler = FlourHandler()
    milk_handler = MilkHandler()
    sugar_handler = SugarHandler()
    oil_handler = OilHandler()
    butter_handler = ButterHandler()

    egg_handler.set_next(flour_handler).set_next(milk_handler).\
    set_next(sugar_handler).set_next(oil_handler).set_next(butter_handler)

    egg_handler.handle(fridge)


min_egg_qty = 2
min_flour_amnt = 300
min_milk_vol = 0.5
min_sugar_amnt = 100
min_oil_qty = 10
min_butter_amnt = 120


some_fridge = Fridge(1, 12, 20, 99, 9, 150)
check_fridge(some_fridge)
