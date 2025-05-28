import math
import time
import random

# Часть работы Семёна
class Percolation: # Класс с методом отслеживания связи ячеек quick_find
    def __init__(self, N, method): # Инициализация
        if N < 1:
            raise ValueError

        self.N = N #Размер сетки просачивания
        self.method = method #Quick_find или Quick_union

        self.grid = [[False for _ in range(1, N + 1)] for _ in range(1, N + 1)] # Наша сетка просачивания

        self.virtual_top = N * N + 1 # Виртуальный верхний элемент, связанный со всеми верхними элементами
        self.virtual_bottom = N * N + 2 # Виртуальный нижний элемент, связанный со всеми нижними элементами

        self.parent = [i for i in range(N * N + 3)] # Массив корней компонентов связности (+3 из-за виртуальных элементов)
        self.size = [1] * (N * N + 3)  # Вес компоненты (для весовой эвристики)

        # Связываем наши виртуальные элементы со всеми верхними и нижними элементами соответственно
        for i in range(1, N + 1):
            self._union(self._index(1, i), self.virtual_top)
            self._union(self._index(N, i), self.virtual_bottom)

    def _index(self, i, j): # Возвращает число - одномерный индекс элемента
        if i < 1 or i > self.N or j < 1 or j > self.N: #Элемент вне сетки
            raise ValueError
        return (i - 1) * self.N + j # Процесс перевода

    def _find(self, x): # Возвращает корень элемента х (quick_find)
        if self.method == "quick_find":
            return self.parent[x]
        else:
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]  # Сжатие пути
                x = self.parent[x]
            return x

    def _union(self, x, y): # Объединяет элементы х и у в одну компоненту связности (quick_find)
        root_x = self._find(x)
        root_y = self._find(y)
        if root_x == root_y:
            return
        if self.method == "quick_find":
            if root_x != root_y:
                for i in range(len(self.parent)):
                    if self.parent[i] == root_y:
                        self.parent[i] = root_x
        else:
            # Весовая эвристика: меньший корень подвешиваем к большему
            if self.size[root_x] < self.size[root_y]:
                self.parent[root_x] = root_y
                self.size[root_y] += self.size[root_x]
            else:
                self.parent[root_y] = root_x
                self.size[root_x] += self.size[root_y]

    def open(self, i, j): # Открывает ячейку
        if not self.isOpen(i, j):
            self.grid[i - 1][j - 1] = True

        # Проверяем соседей (вверх, вниз, влево, вправо)
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 1 <= ni <= self.N and 1 <= nj <= self.N and self.isOpen(ni, nj):
                self._union(self._index(i, j), self._index(ni, nj)) # Связываем элемент с соседями

    def isOpen(self, i, j): # Проверяем открыта ячейка или нет
        if not (1 <= i <= self.N and 1 <= j <= self.N):
            raise ValueError
        return self.grid[i - 1][j - 1]

    def isFull(self, i, j): # Проверяем заполнена ли ячейка (открыта и связана с верхней открытой ячейкой)
        return self.isOpen(i, j) and self._find(self._index(i, j)) == self._find(self.virtual_top)

    def percolates(self): # Проверка просачивания
        return self._find(self.virtual_top) == self._find(self.virtual_bottom)

#Часть работы Анатолия
class PercolationStats:
    def __init__(self, n, t, method):
        self.n = n #Размер сетки просачивания
        self.t = t #Количество экспериментов
        self.method = method #Используемая структура
    def doExperiment(self): #Основной цикл
        if self.n <= 0 or self.t <= 0:
            raise ValueError("N и T должны быть больше 0")
        self.results = [] #Список результатов (долей открытых ячеек)
        for _ in range(self.t): #Проводим t экспериментов
            perc = Percolation(self.n, self.method)
            opened = 0
            while not perc.percolates(): #Пока система не просачивается
                i, j = random.randint(1, self.n), random.randint(1, self.n) #Выбираем случайную ячейку
                if not perc.isOpen(i, j):
                    perc.open(i, j) #Открываем случайную ячейку
                    opened += 1 #Счетчик открытых
            self.results.append(opened / (self.n * self.n)) #Добавляем в список результатов получившийся порог просачивания

    def mean(self): #Подсчёт выборного среднего
        return sum(self.results) / self.t

    def stddev(self): #Подсчет стандартного отклонения
        mu = self.mean()
        return math.sqrt(sum((x - mu) ** 2 for x in self.results) / (self.t - 1))

    def confidence(self): #Подсчёт доверительного интервала
        mu = self.mean()
        sigma = self.stddev()
        margin = 1.96 * sigma / math.sqrt(self.t)
        return mu - margin, mu + margin

    def print_stats(self): # Вывод статистики
        print(f"Выборочное среднее = {self.mean()}")
        print(f"Стандартное отклонение = {self.stddev()}")
        print(f"Доверительный интервал = {self.confidence()}")

#######################################################################################################################
#Проверка работы двух структур, наглядное измерение изменения времени их работы (выполнено Семёном)
print("Тесты Монте Карло:")

PS = PercolationStats(40, 100, method = "quick_find")
start_time = time.time() #Засекаем начальное время
print("Просачивание с методом quick_find")
PS.doExperiment()
end_time = time.time()  #Засекаем конечное время
elapsed_time = end_time - start_time  #Вычисляем разницу

PS.print_stats()

print(elapsed_time)


print()


PS = PercolationStats(80, 100, method = "quick_union")
start_time = time.time()
print("Просачивание с методом quick_union")
PS.doExperiment()
end_time = time.time()
elapsed_time = end_time - start_time

PS.print_stats()

print(elapsed_time)
