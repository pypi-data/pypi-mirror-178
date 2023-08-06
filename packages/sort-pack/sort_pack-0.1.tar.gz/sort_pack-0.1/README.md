# Практическая работа №6 – Модульные программы

**Тетюшкин Максим**,
**КИ22-16/1Б**,
**Вариант 21**

`$ python sort_pack --help` — помощь с работой программы

`$ python sort_pack --test` — вызов тестов

`$ python sort_pack --list 1 2 4 2 3` — сортировка списка [1 2 4 2 3]

`$ python sort_pack --random 10` — сортировка случайного списка длиной 10

Пример использования пакета:

```python
from sort_pack.sort_counting import sort_list
print(sort_list([3, 5, 9, 1, 0]))
```

`[0, 1, 3, 5, 9]`
