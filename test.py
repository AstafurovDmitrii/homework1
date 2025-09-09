""" total = 0  # Сюда будем суммировать числа

for i in range(10):
    num = int(input(f"Введите число {i+1}: "))  # Запрашиваем число
    total += num  # Увеличиваем сумму

print(f"Сумма: {total}")  # Выводим результат """ 


"""list = [10, -5, 3, -2]
list_new = []

for num in list:
    if num > 0:
        list_new.append(num)

print(list_new)"""


"""list = [1, 2, 2, 3, 4, 4]
list_new = []

for num in list:
    if list.count(num) > 1 and num not in list_new:
        list_new.append(num)

print(list_new)"""

"""list = [1, 2, 2, 3, 4, 4]
list_new = set()
seem = set()

for num in list:
    if num in seem:
        list_new.add(num)
    else:
        seem.add(num)

print(list_new)"""


"""book_1 = {'a':True, 'b':False, 'c':True}
book_2 = []

for key, value in book_1.items():
    if value == True:
        book_2.append(key)

print(book_2)"""


animals = ['cat', 'dog', 'parrot', 'dog', 'fish']
animals.remove("dog")
print(animals)

nums = [42, 17, 99, 5, 23]
nums.sort()
print(nums)
nums.sort(reverse=True)
print(nums)
frutes = ['apple', 'kiwi', 'banana']
frutes.sort(key=len)#


num = [1, 2, 3, 2, 1, 4, 5]
while 2 in num:
    num.remove(2)#Удалите все двойки
num.sort(reverse=True)# список по убыванию.


num = tuple(10, 20, 30, 40, 50)
print(len(num)) # Выведите его длину. 5
print(num.index(30)) # 2


a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a|b)# объединение
print(a - b)#разность a - b


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
print(letters[2:5])# Выведите элементы со 2-го по 5-й.
print(letters[::2])# Выведите каждый второй элемент.
print(letters[::-1])#Разверните список задом наперёд.


def is_even(num):
    if num %2 == 0:
        print()
    else:
        print()


numbers = [1, 2, 3, 4]
new_numbers = list(map(lambda x: x + 10, numbers))
print(new_numbers)  # [11, 12, 13, 14]


words = ["Apple", "banana", "apricot", "Orange"]
new_word = list(filter(lambda word: word.lower().startswith('a'), words))
print(new_word)  # 


class Book:
    def __init__(self, author, title):  # Конструктор
        self.author = author  # Атрибут экземпляра
        self.title = title

    def display_info(self):  # Метод класса (должен быть внутри класса!)
        print(f"Книга: '{self.title}', автор: {self.author}")

# Создаем объект
book = Book("Nicola", "Doom")
book.display_info()  # Вызываем метод

class Ebook(Book):
    def __init__(self, author, title, year):  # Добавляем year + аргументы родителя
        super().__init__(author, title) 
        self.year = year

    def display_info(self):  # Метод класса (должен быть внутри класса!)
        return f"{super().display_info()}, год: {self.year}"

# Создаем объект
ebook = Ebook("Nicola", "Doom", 2003)
ebook.display_info()  # Вызываем метод


a= 2
b =3 
c = a + b 

int(input("a: "), input("b: "))

print(c = (a + b (int(input("a: "), input("b: ")))))

if a%2 == 0:
    print(nise)
else:
    print(no)



num = int(input("Введите число: "))  # например, 5

for i in range(1, 11):  # от 1 до 10
    total = num * i
    print(f"{num} * {i} = {total}")  # форматированная строка