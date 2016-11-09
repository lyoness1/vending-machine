
class Item(object):
    """Vending maching object."""

    def __init__(self, name, cost=None):
        """Initialize vending machine."""
        self.name = name
        self.cost = cost or _item_costs[item]


class Coin(object):
    """Vending maching object."""

    def __init__(self, value):
        """Initialize vending machine."""
        self.name = str(value)
        self.value = value


class VendingMaching(object):
    """Vending maching object."""

    def __init__(self, id):
        """Initialize Vending machine."""
        self.id = id
        self.change_available = {}
        self.initial_value = self._calculate_worth()
        self.inventory = {} # 
        self.value_entered = 0

    def _set_initial_change(self, coins):
        """Puts all the inital change in the machine."""
        for key, count in coins.iteritems():
            self.change_available[key] = [Coin(int(key)) for _ in xrange(count)]

    def _set_initial_inventory(self, inventory, costs):
        """Puts all the initial items in the machine."""
        for key, count in inventory.iteritems():
            if costs[key]:
                item_cost = costs[key]
            else:
                raise "Item is not available for pre-stocking"
            self.inventory[key] = [Item(key, item_cost) for _ in xrange(count)]

    def _calculate_worth(self):
        """Calculates the total amount of money in the machine."""
        total = 0
        for value, coins in self.change_available.iteritems():
            value = int(value)
            total += value * len(coins)
        return total

    def _calculate_profit(self):
        """Calculates how much profit machine has made."""
        return self.calculate_worth() - self.initial_value

    def remove_item(self, item):
        """Removes an item from machine."""
        
        if item not in self.inventory:
            pass

    def get_money(self, *args):
        """Receives coins. *args = Coin objects."""
        for coin in args:
            self.value_entered += coin.value

    def take_order(self, item_name):
        """Gets an order for an item, tried to return item and change."""
        # check if item is in inventory
        try:
            item = self.inventory[item_name].pop()
        except InventoryException:
            return "Item is not currently in stock."

        # check if sufficient funds have been entered
        if self.value_entered < item.cost:
            raise InsufficientFundsException()
            return "Insufficient funds for purchase."

        # purchase item
        self.value_entered -= item.cost

        # if change needed -
        # return change and item if change can be made, or 
        # return original value of money inserted into machine with error msg
        if self.value_entered:
            try:
                change = self.return_change(self.value_entered)
                return item, change

            except ChangeException:
                self.value_entered += item.cost
                change = self.return_change(self.value_entered)
                return "Proper change cannot be made for that item."

        # No change needed - return item
        return item

    def return_change(self, change_needed):
        """Returns change in the amount specified."""

        ret = []

        coin_values = map(int, self.change_available.keys())
        coin_values.sort(reverse=True) # [25, 10, 5, 1]

        while change_needed:
            for value in coin_values:
                while change_needed >= value and self.change_available[str(value)]:
                    coin = self.change_available[str(value)].pop()
                    change_needed -= coin.value
                    ret.append(coin)

        self.value_entered -= change_needed
        return ret


class Factory(object):
    """A vending machine factory."""

    def __init__(self):
        self.machine_count = 0
        self.machines = []

    def make_machine(self, initial_change, items_inventory, item_costs):
        machine = VendingMaching(self.machine_count)
        self.set_initial_change(machine, initial_change)
        self.set_initial_inventory(machine, items_inventory, item_costs)
        self.machines.append(machine)
        self.machine_count += 1
        return machine

    def set_initial_change(self, machine, coins):
        """Give a machine its initial change."""
        return machine._set_initial_change(coins)

    def set_initial_inventory(self, machine, items_inventory, item_costs):
        """Give a machine it's initial inventory."""
        return machine._set_initial_inventory(items_inventory, item_costs)

    def reset(self):
        """Return profit (if any), and refill change/items to initial values."""
        profit = self.machine._calculate_profit()


class ChangeException(Exception):
    """Raised when not enough change is available in machine."""

class InventoryException(Exception):
    """Raised when items are out of stock."""
    
class InsufficientFundsException(Exception):
    """Raised when not enough money has been entered for desired purchase."""



if __name__ == '__main__':
    
    # Variables for tests
    _initial_coin_inventory = {
        "1": 100,
        "5": 100,
        "10": 100,
        "25": 200
    }
    _initial_item_inventory = {
        "candy": 1,
        "snack": 10,
        "nuts": 5,
        "coke": 10,
        "pepsi": 10,
        "diet": 15
    }
    _item_costs = {
        "candy": 10,
        "snack": 50,
        "nuts": 90,
        "coke": 25,
        "pepsi": 35,
        "diet": 45
    }

    # Test set-up of machines in factory
    factory = Factory()
    machine0 = factory.make_machine(_initial_coin_inventory,
                                     _initial_item_inventory,
                                     _item_costs)
    machine1 = factory.make_machine(_initial_coin_inventory,
                                     _initial_item_inventory,
                                     _item_costs)

    print "\nMachines: ", [machine.id for machine in factory.machines]
    print "\nMachine", machine1.id, "initial worth: ", machine1._calculate_worth()

    print "\nMachine 1 inventory: "
    for k, v in machine1.inventory.iteritems():
        print k, ":", len(v)

    print "\nMachine1 change available: "
    for k, v in machine1.change_available.iteritems():
        print k, ":", len(v)

    # Test inserting money into machine
    machine1.get_money(Coin(25), Coin(25), Coin(10))
    print "\nChage entered: ", machine1.value_entered

    # Test making order, getting item and change
    order = machine1.take_order("snack")
    if len(order):
        print "Order: ", order[0].name
        print "Change: ", [coin.value for coin in order[1]]
    else:
        print "Order: ", order.name

