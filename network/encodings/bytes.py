data_str = 'Some str text'

data_bytes = b'Some bytes text'


to_bytes = data_str.encode()

to_string = data_bytes.decode()


from_bytes = to_bytes.decode()

from_string = to_string.encode()


# Выводим исходный содержимое строки и байтов на экран
print(data_str)

print(data_bytes)


# Выводим исходный содержимое преобразованных строки и байтов на экран
print(to_bytes)

print(to_string)


# Выводим исходный содержимое преобразованных обратно строки и байтов на экран
# Преобразование строк в байты и байтов в строки не сопровождается потерей данных
print(from_bytes)

print(from_string)



