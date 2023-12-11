a = ['Материал', 'Тип', 'Способ']
o = ['Диаметр', 'Сечение']
n = None
#

# b = []
#
# b += filter(None, *[a])
# b += filter(None, [n])
# b += filter(None, *[o])
#
# print(b)
#
# b = []
#
# b += [a] if a is not None else []
# b += [n] if a is not None else []
# b += [o] if a is not None else []
# print(b)
#
b = []

x = {'Комплект': ('Электронный с таймерным выходом', 'Времени программное'), 'Расположение': ('На стене',), 'Тип': ('Ответвительная', 'Трансляции минутных импульсов', 'Стц-1', '2рвм'), 'Элемент': ('Секундомер', 'Коробка', 'Реле')}
xk = list(x.keys())
xks = sorted(x.keys())
print(xk)

(b.extend(xk) if a is not None else None)
(b.extend(o) if o is not None else None)
(b.extend(n) if n is not None else None)
print(b)