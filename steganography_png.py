import numpy as np
from PIL import Image
import sys


def lsb_hide(image, text):
    """Скрытие текста в младших битах."""
    binary_text = ''.join(format(ord(char), '08b') for char in text) + '00000000'  # Завершение строки
    data = np.array(image)
    height, width, _ = data.shape

    idx = 0
    for i in range(height):
        for j in range(width):
            for k in range(3):  # RGB
                if idx < len(binary_text):
                    data[i, j, k] = (data[i, j, k] & ~1) | int(binary_text[idx])
                    idx += 1

    return Image.fromarray(data)


def lsb_extract(image):
    """Извлечение текста из младших битов."""
    data = np.array(image)
    binary_text = ""
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(3):  # RGB
                binary_text += str(data[i, j, k] & 1)

    text = ''.join(chr(int(binary_text[i:i + 8], 2)) for i in range(0, len(binary_text), 8))
    return text.split('\x00')[0]  # Удаляем завершение


def channel_hide(image, text, channel_index):
    """Скрытие текста в заданном канале (красный, зелёный, синий, альфа)."""
    binary_text = ''.join(format(ord(char), '08b') for char in text) + '00000000'
    data = np.array(image)
    idx = 0

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if idx < len(binary_text):
                data[i, j, channel_index] = (data[i, j, channel_index] & ~1) | int(binary_text[idx])
                idx += 1

    return Image.fromarray(data)


def channel_extract(image, channel_index):
    """Извлечение текста из заданного канала."""
    data = np.array(image)
    binary_text = ""

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            binary_text += str(data[i, j, channel_index] & 1)

    text = ''.join(chr(int(binary_text[i:i + 8], 2)) for i in range(0, len(binary_text), 8))
    return text.split('\x00')[0]


def menu():
    print("\nВыберите метод:")
    print("1. LSB (Least Significant Bit)")
    print("2. Скрытие в красном канале")
    print("3. Скрытие в зелёном канале")
    print("4. Скрытие в синем канале")
    print("5. Скрытие в альфа-канале")
    print("6. Извлечение текста (LSB)")
    print("7. Извлечение текста из красного канала")
    print("8. Извлечение текста из зелёного канала")
    print("9. Извлечение текста из синего канала")
    print("10. Извлечение текста из альфа-канала")
    print("11. Выход")


def main():
    while True:
        menu()
        choice = input("Введите номер метода: ")
        if choice == '1':
            img_path = input("Введите путь к изображению: ")
            text = input("Введите текст для сокрытия: ")
            output_path = input("Введите имя выходного файла: ")
            image = Image.open(img_path)
            result = lsb_hide(image, text)
            result.save(output_path)
            print("Текст успешно скрыт!")
        elif choice in ['2', '3', '4', '5']:
            channel_names = ['красный', 'зелёный', 'синий', 'альфа']
            channel_index = int(choice) - 2
            img_path = input("Введите путь к изображению: ")
            text = input("Введите текст для сокрытия: ")
            output_path = input("Введите имя выходного файла: ")
            image = Image.open(img_path)
            if channel_index == 3 and image.mode != 'RGBA':
                image = image.convert('RGBA')  # Убедимся, что есть альфа-канал
            result = channel_hide(image, text, channel_index)
            result.save(output_path)
            print(f"Текст успешно скрыт в {channel_names[channel_index]} канале!")
        elif choice in ['6', '7', '8', '9', '10']:
            channel_names = ['LSB', 'красный', 'зелёный', 'синий', 'альфа']
            channel_index = int(choice) - 6
            img_path = input("Введите путь к изображению: ")
            image = Image.open(img_path)
            if channel_index == 4 and image.mode != 'RGBA':
                image = image.convert('RGBA')  # Убедимся, что есть альфа-канал
            if channel_index == 0:
                text = lsb_extract(image)
            else:
                text = channel_extract(image, channel_index - 1)
            print(f"Извлечённый текст ({channel_names[channel_index]} канал): {text}")
        elif choice == '11':
            print("Выход из программы.")
            sys.exit()
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == '__main__':
    main()
