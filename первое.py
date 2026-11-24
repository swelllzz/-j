class Animal:
    """Родительский класс."""

    def __init__(self, name, species, age, weight, habitat):
        self.name = name          # кличка
        self.species = species    # вид
        self.age = age            # возраст (лет)
        self.weight = weight      # вес (кг)
        self.habitat = habitat    # среда обитания

    def info(self):
        return (f"{self.name} ({self.species}), {self.age} лет, "
                f"{self.weight} кг, среда обитания: {self.habitat}")

    def eat(self, food):
        return f"{self.name} с аппетитом ест: {food}."


class Reptile(Animal):
    """Пресмыкающиеся."""

    def __init__(self, name, species, age, weight, habitat,
                 is_venomous, body_length, skin_type):
        super().__init__(name, species, age, weight, habitat)
        self.is_venomous = is_venomous    # ядовитое ли
        self.body_length = body_length    # длина тела (м)
        self.skin_type = skin_type        # тип покрова

    def bask_in_sun(self):
        return f"{self.name} греется на солнышке, чтобы поднять температуру тела."

    def shed_skin(self):
        return f"{self.name} линяет: старая кожа ({self.skin_type}) сброшена!"


class Amphibian(Animal):
    """Земноводные."""

    def __init__(self, name, species, age, weight, habitat,
                 skin_moisture, can_jump, lays_eggs_in_water):
        super().__init__(name, species, age, weight, habitat)
        self.skin_moisture = skin_moisture            # влажность кожи (%)
        self.can_jump = can_jump                      # умеет ли прыгать
        self.lays_eggs_in_water = lays_eggs_in_water  # откладывает икру в воду

    def swim(self):
        return f"{self.name} ловко плавает в воде."

    def croak(self):
        return f"{self.name} громко квакает на весь зоопарк!"


class ZooShow:
    """Шоу в зоопарке с выбором типа, билетов и мест."""

    TICKET_PRICES = {"vip": 5000, "regular": 2000}   # цена в тенге/сом/руб. — на ваше усмотрение
    CURRENCY = "сом"

    def __init__(self):
        self.reptiles = [
            Reptile("Каа", "Удав", 6, 25, "Тропики", False, 3.5, "чешуя"),
            Reptile("Рэмбо", "Крокодил", 12, 180, "Река", True, 4.0, "роговые пластины"),
            Reptile("Гоша", "Игуана", 4, 6, "Лес", False, 1.2, "чешуя"),
        ]
        self.amphibians = [
            Amphibian("Квака", "Древесная лягушка", 2, 0.05, "Лес", 80, True, True),
            Amphibian("Тритон Тим", "Тритон", 3, 0.03, "Пруд", 75, False, True),
            Amphibian("Жаба Берта", "Жаба", 5, 0.2, "Болото", 70, True, True),
        ]

    def show_prices(self):
        print("\n=== Цены на билеты ===")
        print(f"VIP (первые ряды): {self.TICKET_PRICES['vip']} {self.CURRENCY}")
        print(f"Обычный (задние ряды): {self.TICKET_PRICES['regular']} {self.CURRENCY}")

    def _ask(self, prompt, options):
        while True:
            answer = input(prompt).strip()
            if answer in options:
                return answer
            print("Неверный ввод, попробуйте ещё раз.")

    def _ask_int(self, prompt, low, high):
        while True:
            answer = input(prompt).strip()
            if answer.isdigit() and low <= int(answer) <= high:
                return int(answer)
            print(f"Введите число от {low} до {high}.")

    def run_program(self, show_type):
        if show_type == "1":
            title = "ШОУ ПРЕСМЫКАЮЩИХСЯ"
            a, b, c = self.reptiles
            lines = [
                a.info(), a.eat("кролика"), a.bask_in_sun(),
                b.info(), b.shed_skin(),
                c.info(), c.bask_in_sun(),
            ]
            description = (f"{a.name} покажет танец на ветке, {b.name} откроет пасть "
                           f"перед дрессировщиком, а {c.name} пройдёт по канату.")
        else:
            title = "ШОУ ЗЕМНОВОДНЫХ"
            a, b, c = self.amphibians
            lines = [
                a.info(), a.croak(), a.eat("мух"),
                b.info(), b.swim(),
                c.info(), c.croak(),
            ]
            description = (f"{a.name} выполнит прыжки через обруч, {b.name} "
                           f"устроит заплыв, а {c.name} даст хоровое кваканье.")
        return title, lines, description

    def start(self):
        print("Добро пожаловать на шоу в зоопарке!")
        self.show_prices()

        print("\nКакое шоу хотите посмотреть?")
        print("1 — Пресмыкающиеся")
        print("2 — Земноводные")
        show_type = self._ask("Ваш выбор: ", ("1", "2"))

        title, lines, description = self.run_program(show_type)
        print(f"\n--- Программа: {title} ---")
        for line in lines:
            print(" •", line)

        print("\nТип билета:")
        print(f"1 — VIP ({self.TICKET_PRICES['vip']} {self.CURRENCY})")
        print(f"2 — Обычный ({self.TICKET_PRICES['regular']} {self.CURRENCY})")
        ticket = self._ask("Ваш выбор: ", ("1", "2"))
        ticket_key = "vip" if ticket == "1" else "regular"

        if ticket_key == "vip":
            seat_range = (1, 20)    # первые ряды
        else:
            seat_range = (21, 100)  # задние ряды
        seat = self._ask_int(
            f"Выберите место ({seat_range[0]}-{seat_range[1]}): ", *seat_range)
        count = self._ask_int("Сколько билетов (1-10): ", 1, 10)

        total = self.TICKET_PRICES[ticket_key] * count
        ticket_name = "VIP" if ticket_key == "vip" else "Обычный"

        print("\n" + "=" * 40)
        print(f'"{title}"')
        print(description)
        print(f"Билет: {ticket_name}, место №{seat}, количество: {count}")
        print(f"К оплате: {total} {self.CURRENCY}")
        print("=" * 40)
        print("Приятного просмотра!")


if __name__ == "__main__":
    ZooShow().start()