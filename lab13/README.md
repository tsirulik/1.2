# Лабораторная работа №13
## ООП. Классы и объекты
### Задания для самостоятельного выполнения
Перепишите свой вариант лабораторной работы №12 с использованием классов и объектов.

Задание то же, вариант GUI фреймворка возьмите следующий по списку.

В коде должны присутствовать:

+ абстрактный базовый класс и соотвествующие декораторы для методов
+ иерархия наследования
+ managed - атрибуты
+ минимум 2 dunder-метода у подклассов


```python
 from math import pi
from scipy.constants import c, e, h, m_e, m_n, m_p

class Particle:
    """Базовый класс для элементарных частиц."""

    def __init__(self, name, mass, charge):
        """
        Инициализирует объект частицы.

        Args:
            name (str): Имя частицы.
            mass (float): Масса частицы в кг.
            charge (float): Заряд частицы в Кулонах.
        """

        self.name = name
        self.mass = mass
        self.charge = charge

    def specific_charge(self):
        """
        Возвращает удельный заряд частицы.

        Returns:
            float: Удельный заряд частицы.
        """

        return self.charge / self.mass

    def compton_wavelength(self):
        """
        Возвращает комптоновскую длину волны частицы.

        Returns:
            float: Комптоновская длина волны частицы.
        """

        return h / (m_e * c)

    def __str__(self):
        """
        Возвращает строковое представление частицы.

        Returns:
            str: Строковое представление частицы.
        """

        return f"Частица: {self.name}, Масса: {self.mass} кг, Заряд: {self.charge} Кл"

class Electron(Particle):
    """Класс для электрона."""

    def __init__(self):
        """
        Инициализирует объект электрона.
        """

        super().__init__("Электрон", m_e, -e)

class Neutron(Particle):
    """Класс для нейтрона."""

    def __init__(self):
        """
        Инициализирует объект нейтрона.
        """

        super().__init__("Нейтрон", m_n, 0)

class Proton(Particle):
    """Класс для протона."""

    def __init__(self):
        """
        Инициализирует объект протона.
        """

        super().__init__("Протон", m_p, e)

# Создание объектов частиц
electron = Electron()
neutron = Neutron()
proton = Proton()

# Вывод информации о частицах
print(electron)
print(f"Удельный заряд электрона: {electron.specific_charge()} Кл/кг")
print(f"Комптоновская длина волны электрона: {electron.compton_wavelength()} м")

print(neutron)
print(f"Удельный заряд нейтрона: {neutron.specific_charge()} Кл/кг")
print(f"Комптоновская длина волны нейтрона: {neutron.compton_wavelength()} м")

print(proton)
print(f"Удельный заряд протона: {proton.specific_charge()} Кл/кг")
print(f"Комптоновская длина волны протона: {proton.compton_wavelength()} м")
 

````

