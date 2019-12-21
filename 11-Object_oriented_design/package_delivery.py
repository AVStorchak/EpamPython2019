from abc import ABC, abstractmethod
import queue


class Warehouse(ABC):
    @abstractmethod
    def dispatch_shipment(self):
        transport = min(self.fleet, key=self.fleet.get)
        package = self.stock.popleft()

        if transport.time_en_route < package[1]:
            transport.time_en_route = package[1]
        else:
            package[1] = transport.time_en_route

        if FinalWarehouse.warehouses[package[0]].transfer_warehouse is None or\
           FinalWarehouse.warehouses[package[0]].transfer_warehouse == self:
            address = FinalWarehouse.warehouses[package[0]]
        else:
            address = FinalWarehouse.warehouses[package[0]].transfer_warehouse

        transport.deliver(package, address)


class BaseWarehouse(Warehouse):
    def __init__(self, stock):
        self.fleet = {}
        packages = [[i, 0] for i in stock]
        self.stock = queue.deque(packages)

    def dispatch_shipment(self):
        super().dispatch_shipment()


class TransferWarehouse(Warehouse):
    def __init__(self, delivery_time):
        self.fleet = {}
        self.delivery_time = delivery_time
        self.stock = queue.deque()

    def dispatch_shipment(self):
        super().dispatch_shipment()


class FinalWarehouse(Warehouse):
    warehouses = {}

    def __init__(self, code, delivery_time, transfer_warehouse=None):
        self.warehouses[code] = self
        self.delivery_time = delivery_time
        self.transfer_warehouse = transfer_warehouse
        self.stock = queue.deque()

    def dispatch_shipment():
        pass


class Transport(ABC):
    @abstractmethod
    def __init__(self, operating_base):
        self.operating_base = operating_base
        self.time_en_route = 0
        self.operating_base.fleet[self] = self.time_en_route

    @abstractmethod
    def deliver(self, package, address):
        package[1] += address.delivery_time
        address.stock.append(package)
        self.time_en_route += 2*address.delivery_time
        self.operating_base.fleet[self] = self.time_en_route


class Truck(Transport):
    def __init__(self, operating_base):
        super().__init__(operating_base)

    def deliver(self, package, address):
        super().deliver(package, address)


class Ship(Transport):
    def __init__(self, operating_base):
        super().__init__(operating_base)

    def deliver(self, package, address):
        super().deliver(package, address)


if __name__ == '__main__':
    delivery_order = 'ABBBABAAABBB'
    factory = BaseWarehouse(delivery_order)
    port = TransferWarehouse(1)
    warehouse_a = FinalWarehouse('A', 4, port)
    warehouse_b = FinalWarehouse('B', 5)
    truck_1 = Truck(factory)
    truck_2 = Truck(factory)
    ship_1 = Ship(port)

    while factory.stock:
        factory.dispatch_shipment()

    while port.stock:
        port.dispatch_shipment()

    print("Total delivery time is",
          max(warehouse_a.stock[-1][1], warehouse_b.stock[-1][1]))
