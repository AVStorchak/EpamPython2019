import queue


class BaseWarehouse:
    """
    This is a class for warehouses that operate as dispatch points.

    Attributes:
        fleet: Dictionary of transport units operating from the warehouse,
        dictionary keys are Transport class objects, dictionary values are
        actual operation times for such Transport class objects.
        stock: Queue of packages to be dispatched, each package has
        a format of [destination, delivery_time], where destination is the
        code of the final warehouse for the package, delivery_time is
        absolute time of an operation with the package (delivery to the final or
        to the transfer warehouse).
    """
    def __init__(self, stock):
        self.fleet = {}
        packages = [[i, 0] for i in stock]
        self.stock = queue.deque(packages)

    def dispatch_shipment(self):
        """
        The function to dispatch a package to the specified address
        by calling the deliver function of the Transport class.

        Parameters:
            package: The next package from the queue
            transport: The transport unit is selected from the
            fleet by the lowest time en route.
            address: The address is derived from the dictionary of final
            warehouses and their codes. If the final warehouse must be
            reached via a transfer warehouse, such transfer warehouse is
            selected as the current package address.
        """
        transport = min(self.fleet, key=self.fleet.get)
        package = self.stock.popleft()

        if FinalWarehouse.warehouses[package[0]].transfer_warehouse is None or \
           FinalWarehouse.warehouses[package[0]].transfer_warehouse == self:
            address = FinalWarehouse.warehouses[package[0]]
        else:
            address = FinalWarehouse.warehouses[package[0]].transfer_warehouse

        transport.deliver(package, address)


class TransferWarehouse(BaseWarehouse):
    """
    This is a child class of the BaseWarehouse class. Since transfer warehouses
    do not have initial stock and are located at some distance from base
    warehouses, the __init__ method was changed accordingly.
    """
    def __init__(self, delivery_time):
        self.fleet = {}
        self.delivery_time = delivery_time
        self.stock = queue.deque()


class FinalWarehouse:
    """
    This is a class for warehouses that are final destinations for packages.

    Attributes:
        final_warehouses: Class attribute to keep record of final
        warehouses and their codes.
        delivery_time: Time of package delivery to the warehouse, counted
        from the nearest dispatch point.
        transfer_warehouse: The transfer warehouse connected with the final
        warehouse (where available).
        stock: The queue of incoming packages.
    """
    warehouses = {}

    def __init__(self, code, delivery_time, transfer_warehouse=None):
        self.warehouses[code] = self
        self.delivery_time = delivery_time
        self.transfer_warehouse = transfer_warehouse
        self.stock = queue.deque()

    def get_time(self):
        """
        The function to get the arrival time of the latest package.
        Returns 0 if there are no packages.
        """
        try:
            time = self.stock[-1][1]
        except IndexError:
            time = 0
        return time


class Transport:
    """
    This is a class for transport vehicles that operate from base
    warehouses and deliver packages.

    Attributes:
        operating_base: The base warehouse to which the transport unit
        is assigned.
        time_en_route: The cumulative transport unit travel time.
    """
    def __init__(self, operating_base):
        self.operating_base = operating_base
        self.time_en_route = 0
        self.operating_base.fleet[self] = self.time_en_route

    def deliver(self, package, address):
        """
        The function to deliver a package to the specified address.
        If the transport unit has been idle for some period, the parameter is
        adjusted accordingly using the package delivery time.
        When the delivery is finished, the fleet status of the transport unit
        is updated.

        Parameters:
            package: Is passed by the base warehouse along with the address.
            delivery_time: Is taken from the destination point and is used to
            update the transport time en route and the package delivery time.
        """
        if self.time_en_route < package[1]:
            self.time_en_route = package[1]
        else:
            package[1] = self.time_en_route

        package[1] += address.delivery_time
        address.stock.append(package)
        print(f'Package delivered to {address}, timestamp {package[1]}')

        self.time_en_route += 2*address.delivery_time
        self.operating_base.fleet[self] = self.time_en_route


if __name__ == '__main__':
    delivery_order = input("Please provide the delivery order ")
    factory = BaseWarehouse(delivery_order)
    port = TransferWarehouse(1)
    warehouse_a = FinalWarehouse('A', 4, port)
    warehouse_b = FinalWarehouse('B', 5)
    truck_1 = Transport(factory)
    truck_2 = Transport(factory)
    ship_1 = Transport(port)

    while factory.stock:
        factory.dispatch_shipment()

    while port.stock:
        port.dispatch_shipment()

    print("Total delivery time is", max(warehouse_a.get_time(),
                                        warehouse_b.get_time()))
