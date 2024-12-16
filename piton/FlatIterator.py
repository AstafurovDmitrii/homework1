class FlatIterator:
    def __init__(self, list_of_lists):
        # Сохраняем список списков
        self.list_of_lists = list_of_lists
        # Индексы для итерации
        self.outer_idx = 0  # внешний индекс для списка списков
        self.inner_idx = 0  # внутренний индекс для элементов списка

    def __iter__(self):
        return self

    def __next__(self):
        # Пока внешний индекс не вышел за границы списка списков
        while self.outer_idx < len(self.list_of_lists):
            # Текущий подсписок
            current_list = self.list_of_lists[self.outer_idx]

            # Если внутренний индекс в пределах текущего списка
            if self.inner_idx < len(current_list):
                item = current_list[self.inner_idx]  # Берем текущий элемент
                self.inner_idx += 1  # Сдвигаем внутренний индекс
                return item
            else:
                # Переходим к следующему подсписку
                self.outer_idx += 1
                self.inner_idx = 0  # Сбрасываем внутренний индекс в начало
        # Если элементы закончились
        raise StopIteration


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

if __name__ == '__main__':
    test_1()

import types

def flat_generator(list_of_lists):
    for sublist in list_of_lists:  # Проходим по каждому подсписку
        for item in sublist:       # Проходим по каждому элементу в подсписке
            yield item             # Возвращаем элемент

def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)

if __name__ == '__main__':
    test_2()
