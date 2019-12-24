import queue


class BaseWarehouse:
    """
    This is a class for warehouses that operate as dispatch points.
    Attributes:
        fleet: List transport units operating from the warehouse,
        stock: Queue of packages to be dispatched
    """
    def __init__(self, stock, *transport_units):
        self.fleet = [*transport_units]
        packages = [[i, 0] for i in stock]
        self.stock = queue.deque(packages)

    def dispatch_shipment(self, logistics):
        """
        The function to dispatch a package to the specified address
        by calling the deliver function of the Transport class.
        Parameters:
            package: The next package from the queue
            transport: The transport unit is selected from the
            fleet by the lowest time en route.
            address: The address is derived from the dictionary of final
            warehouses and their codes.
        """
        self.fleet = sorted(self.fleet, key=lambda x: x.time_en_route)
        transport = self.fleet[0]
        package = self.stock.popleft()

        if logistics.structure[package[0]].transfer_warehouse is None or \
           logistics.structure[package[0]].transfer_warehouse == self:
            address = logistics.structure[package[0]]
        else:
            address = logistics.structure[package[0]].transfer_warehouse

        transport.deliver(package, address)


class TransferWarehouse(BaseWarehouse):
    """
    This is a child class of the BaseWarehouse class. Since transfer warehouses
    do not have initial stock and are located at some distance from base
    warehouses, the __init__ method was changed accordingly.
    """
    def __init__(self, delivery_time, *transport_units):
        self.fleet = {}
        self.delivery_time = delivery_time
        self.stock = queue.deque()
        for unit in transport_units:
            self.fleet[unit] = unit.time_en_route


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
    global final_warehouses

    def __init__(self, code, delivery_time, transfer_warehouse=None):
        self.code = code
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


class Logistics():
    """
    A class designated to store data on transport connection
    between warehouses.
    """
    def __init__(self, *args):
        self.structure = {}
        for warehouse in args:
            self.structure[warehouse.code] = warehouse


class Transport:
    """
    This is a class for transport vehicles that operate from base
    warehouses and deliver packages.
    Attributes:
        operating_base: The base warehouse to which the transport unit
        is assigned.
        time_en_route: The cumulative transport unit travel time.
    """
    def __init__(self):
        self.time_en_route = 0

    def deliver(self, package, address):
        """
        The function to deliver a package to the specified address.
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


if __name__ == '__main__':
    truck_1 = Transport()
    truck_2 = Transport()
    ship_1 = Transport()

    delivery_order = input("Please provide the delivery order ")
    factory = BaseWarehouse(delivery_order, truck_1, truck_2)
    port = TransferWarehouse(1, ship_1)
    warehouse_a = FinalWarehouse('A', 4, port)
    warehouse_b = FinalWarehouse('B', 5)
    current_logistics = Logistics(warehouse_a, warehouse_b)

    while factory.stock:
        factory.dispatch_shipment(current_logistics)

    while port.stock:
        port.dispatch_shipment(current_logistics)

    print("Total delivery time is", max(warehouse_a.get_time(),
                                        warehouse_b.get_time()))
