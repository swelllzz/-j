from abc import ABC, abstractmethod
from datetime import datetime


# ===================== 1. АБСТРАКЦИЯ =====================

class MenuItem(ABC):
    """Абстрактная позиция меню."""

    def __init__(self, name, base_price):
        self.name = name
        self.base_price = base_price

    @abstractmethod
    def calculatePrice(self):
        """Итоговая стоимость конкретного блюда."""

    def getDisplayName(self):
        return self.name

    def __str__(self):
        return f"{self.getDisplayName()} — {self.calculatePrice():.2f}"


# ===================== 3. ПОЛИМОРФИЗМ: БЛЮДА =====================

class Pizza(MenuItem):
    def __init__(self, name, base_price, size="обычная"):
        super().__init__(name, base_price)
        self.size = size  # "обычная" или "большая"

    def calculatePrice(self):
        if self.size == "большая":
            return self.base_price * 1.30   # +30%
        return self.base_price

    def getDisplayName(self):
        return f"{self.name} ({self.size})"


class Drink(MenuItem):
    def __init__(self, name, base_price, isIce=False):
        super().__init__(name, base_price)
        self.isIce = isIce

    def calculatePrice(self):
        return self.base_price  # лёд цену не меняет

    def getDisplayName(self):
        return f"{self.name} со льдом" if self.isIce else self.name


class ComboSet(MenuItem):
    DISCOUNT = 0.15

    def __init__(self, name, items):
        super().__init__(name, 0)
        self.items = list(items)  # список других MenuItem

    def calculatePrice(self):
        total = sum(item.calculatePrice() for item in self.items)
        return total * (1 - self.DISCOUNT)

    def getDisplayName(self):
        parts = ", ".join(i.getDisplayName() for i in self.items)
        return f"{self.name} [{parts}]"


# ===================== ПОЛИМОРФИЗМ: ОПЛАТА =====================

class PaymentStrategy(ABC):
    @abstractmethod
    def collectPayment(self, amount):
        ...


class CardPayment(PaymentStrategy):
    def __init__(self, card_number, expiry):
        self.card_number = card_number
        self.expiry = expiry  # формат "MM/YY"

    def _is_valid(self):
        try:
            month, year = self.expiry.split("/")
            month, year = int(month), 2000 + int(year)
            if not 1 <= month <= 12:
                return False
        except ValueError:
            return False
        now = datetime.now()
        # карта действует до конца указанного месяца
        return (year, month) >= (now.year, now.month)

    def collectPayment(self, amount):
        if not self._is_valid():
            raise ValueError("Срок действия карты истёк или указан неверно!")
        masked = "**** **** **** " + self.card_number[-4:]
        print(f"Картой {masked} списано {amount:.2f}.")


class CashPayment(PaymentStrategy):
    def collectPayment(self, amount):
        print(f"Оплата наличными курьеру: {amount:.2f}. Приготовьте сумму.")


# ===================== 2. ИНКАПСУЛЯЦИЯ =====================

class Order:
    __STATUSES = ["Новый", "Готовится", "В доставке", "Доставлен"]

    def __init__(self):
        self.__items = []        # приватный список блюд
        self.__status = 0        # приватный индекс статуса
        self.__paid = False

    @property
    def status(self):
        """Статус можно только читать, менять нельзя."""
        return self.__STATUSES[self.__status]

    def nextStep(self):
        if self.__status >= len(self.__STATUSES) - 1:
            raise ValueError("Заказ уже доставлен, дальше некуда.")
        self.__status += 1
        print(f"Статус заказа: {self.status}")

    def addItem(self, item):
        if not isinstance(item, MenuItem):
            raise TypeError("Можно добавлять только позиции меню.")
        if self.__status >= 1:
            raise ValueError(
                f"Нельзя добавить блюдо: заказ уже в статусе «{self.status}».")
        self.__items.append(item)

    def getTotalCost(self):
        return sum(item.calculatePrice() for item in self.__items)

    def pay(self, paymentMethod):
        if not self.__items:
            raise ValueError("Корзина пуста.")
        if self.__paid:
            raise ValueError("Заказ уже оплачен.")
        paymentMethod.collectPayment(self.getTotalCost())
        self.__paid = True

    def show(self):
        print("\n--- Ваш заказ ---")
        for item in self.__items:
            print(" •", item)
        print(f"Итого: {self.getTotalCost():.2f}")
        print(f"Статус: {self.status}")


# ===================== ДЕМОНСТРАЦИЯ =====================

if __name__ == "__main__":
    pizza = Pizza("Маргарита", 500, "большая")
    cola = Drink("Кола", 100, isIce=True)
    combo = ComboSet("Комбо", [Pizza("Пепперони", 450), Drink("Сок", 90)])

    order = Order()
    order.addItem(pizza)
    order.addItem(cola)
    order.addItem(combo)
    order.show()

    # Оплата: любой способ подходит благодаря полиморфизму
    order.pay(CashPayment())

    order.nextStep()  # Готовится
    try:
        order.addItem(Drink("Чай", 80))
    except ValueError as e:
        print("Ошибка:", e)

    order.nextStep()  # В доставке
    order.nextStep()  # Доставлен

    # Проверка карты с истёкшим сроком
    order2 = Order()
    order2.addItem(Drink("Лимонад", 120))
    try:
        order2.pay(CardPayment("1234567812345678", "01/20"))
    except ValueError as e:
        print("Ошибка оплаты:", e)
    order2.pay(CardPayment("1234567812345678", "12/30"))