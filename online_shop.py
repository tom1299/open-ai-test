import re
from typing import Dict


class Item:
    def __init__(self, id: str, name: str, price: float, description: str, supplier: str, category: str):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.supplier = supplier
        self.category = category

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def get_description(self) -> str:
        return self.description

    def get_supplier(self) -> str:
        return self.supplier

    def get_category(self) -> str:
        return self.category

    def __str__(self):
        return f"Item(id={self.id}, name={self.name}, price={self.price}, description={self.description}, supplier={self.supplier}, category={self.category})"


class StockItem(Item):
    def __init__(self, id: str, name: str, price: float, description: str, supplier: str, category: str, quantity: int):
        super().__init__(id, name, price, description, supplier, category)
        self.quantity = quantity

    def get_quantity(self) -> int:
        return self.quantity

    def __str__(self):
        return f"StockItem(id={self.id}, name={self.name}, price={self.price}, description={self.description}, supplier={self.supplier}, category={self.category}, quantity={self.quantity})"


# Refactor the class Stock to use StockItem instead of Item
class Stock:

    def __init__(self):
        self.items = {}

    def add_item(self, item: Item, quantity: int):
        stock_item = StockItem(item.get_id(), item.get_name(), item.get_price(), item.get_description(), item.get_supplier(), item.get_category(), quantity)
        self.items[item.get_id()] = stock_item

    def get_quantity_by_id(self, id: str) -> int:
        return self.items[id].get_quantity()

    def get_quantity_by_name_regex(self, name: str) -> int:
        for item in self.items.values():
            if re.match(name, item.get_name()):
                return item.get_quantity()
        return 0

    def get_quantity_by_description_regex(self, description: str) -> int:
        for item in self.items.values():
            if re.match(description, item.get_description()):
                return item.get_quantity()
        return 0

    def get_items(self) -> [StockItem]:
        return list(self.items.values())

    def __str__(self):
        return f"Stock(items={self.items})"


class Order:

    def __init__(self, id: str, customer_id: str):
        self.id = id
        self.customer_id = customer_id
        self.items = {}

    def add_item(self, item: Item, quantity: int):
        self.items[item.get_id()] = (item, quantity)

    def get_customer_id(self) -> str:
        return self.customer_id

    def get_items(self) -> dict:
        return self.items

    def get_id(self) -> str:
        return self.id

    def __str__(self):
        return f"Order(id={self.id}, customer_id={self.customer_id}, items={self.items})"


class Customer:

    def __init__(self, id: str, name: str, address: dict, order_history: list):
        self.id = id
        self.name = name
        self.address = address
        self.order_history = order_history

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_address(self) -> dict:
        return self.address

    def get_order_history(self) -> list[Order]:
        return self.order_history

    def add_order_to_history(self, order: Order):
        self.order_history.append(order)

    def __str__(self):
        return f"Customer(id={self.id}, name={self.name}, address={self.address})"


# The class OnlineShop represents an online shop that sells items to customers.
class OnlineShop:

    def __init__(self, stock: Stock, customers: list[Customer]):
        self.stock = stock
        self.customers = customers

    def get_stock(self) -> Stock:
        return self.stock

    def get_customers(self) -> list[Customer]:
        return self.customers
