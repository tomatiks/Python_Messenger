data_str = 'Some str text'

# байтовый массив (bytearray) - изменяемый байтовый тип данных 
data_bytearray = bytearray(data_str, 'utf-8')


print(data_bytearray)


# Изменение содержимого байтовых массивов происходит по аналогии с изменением содержимого списков
# В качестве аргументов методы принимают номер добавляемого или удаляемого символа в таблице кодировки
data_bytearray.append(100)

data_bytearray.append(101)


print(data_bytearray)


data_bytearray.remove(100)

data_bytearray.remove(101)


print(data_bytearray)
