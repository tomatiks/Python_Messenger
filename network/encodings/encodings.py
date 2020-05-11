import sys


# Определяем строку, которая содержит латинские символы
# Латинские символы входят в состав всех известных кодировок
LAT_TEXT = 'Latin text'

# Определяем строку, которая содержит кириллические символы
# Кириллические символы входят в состав лишь некоторых кодировок
KIR_TEXT = 'Кириллический текст'


# Байтовое представление кириллического текста, приведенного выше.
KIR_BYTES = b'\xd0\x9a\xd0\xb8\xd1\x80\xd0\xb8\xd0\xbb\xd0\xb8\xd1\x87\xd0\xb5\xd1\x81\xd0\xba\xd0\xb8\xd0\xb9 \xd1\x82\xd0\xb5\xd0\xba\xd1\x81\xd1\x82'


# Latin-1 - одна из кодирокок в состав которых входят симолы из европейских языкв.
LATIN_ENCODING = 'latin-1'

# Unicode (UTF-8) - кодировка, содержащая символы большей части известных и используемых в мире языков.
UTF_ENCODING = 'utf-8'


# Определяем метод для быстрого и наглядного преобразования строки в байты с использованием определенной кодировки
def to_encoding_bytes(text_str, encoding):

    try:

        print('*'*15, encoding, '*'*15)

        # Метод строк encode - используется для приведения строки к байтовому виду, может принимать название кодировки в качестве аргумента
        text_bytes = text_str.encode(encoding)

        # функция sys.getsizeof - используется для определения место, занимаемого объектом в памяти.
        size = sys.getsizeof(text_bytes)

        print(text_bytes)

        print(size)

    except Exception as err:

        print('='*15, 'ERROR', '='*15)

        print(err)

    finally:

        print('\n')
        

def to_encoding_string(text_bytes, encoding):

    try:

        print('*'*15, encoding, '*'*15)

        # Метод строк decode - используется для приведения байтов к строковому виду, может принимать название кодировки в качестве аргумента
        text_str = text_bytes.decode(encoding)

        # функция sys.getsizeof - используется для определения место, занимаемого объектом в памяти.
        size = sys.getsizeof(text_str)

        print(text_str)

        print(size)

    except Exception as err:

        print('='*15, 'ERROR', '='*15)

        print(err)

    finally:

        print('\n')


if __name__ == '__main__':

    # Эксперементируем с преобразованием строк в байты с использованием различного рода кодировок
    to_encoding_bytes(LAT_TEXT, LATIN_ENCODING)

    to_encoding_bytes(LAT_TEXT, UTF_ENCODING)

    to_encoding_bytes(KIR_TEXT, LATIN_ENCODING)

    to_encoding_bytes(KIR_TEXT, UTF_ENCODING)


    # Эксперементируем с преобразованием байтов в строки с использованием различного рода кодировок
    to_encoding_string(KIR_BYTES, LATIN_ENCODING)

    to_encoding_string(KIR_BYTES, UTF_ENCODING)
