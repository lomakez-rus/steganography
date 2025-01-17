import cv2
import numpy as np
import pywt


# 1. LSB (Least Significant Bit)
def embed_message_lsb(image_path, message, output_path):
    """
    Встраивание сообщения методом LSB.
    """
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        print("Ошибка: не удалось загрузить изображение.")
        return

    message_bin = ''.join(format(ord(char), '08b') for char in message) + '00000000'
    flat_image = image.flatten()

    for i, bit in enumerate(message_bin):
        flat_image[i] = (flat_image[i] & ~1) | int(bit)

    encoded_image = flat_image.reshape(image.shape)
    cv2.imwrite(output_path, encoded_image)
    print("Сообщение скрыто методом LSB и сохранено в:", output_path)


def extract_message_lsb(image_path):
    """
    Извлечение сообщения методом LSB.
    """
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        print("Ошибка: не удалось загрузить изображение.")
        return

    flat_image = image.flatten()
    binary_message = [str(flat_image[i] & 1) for i in range(len(flat_image))]
    message_bin = ''.join(binary_message)
    extracted_message = ''
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i+8]
        if byte == '00000000':
            break
        extracted_message += chr(int(byte, 2))
    return extracted_message


# 2. DWT (Discrete Wavelet Transform)
def embed_message_dwt(image_path, message, output_path):
    """
    Встраивание сообщения с использованием DWT.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Ошибка: не удалось загрузить изображение.")
        return

    message_bin = ''.join(format(ord(char), '08b') for char in message) + '00000000'

    coeffs2 = pywt.dwt2(image, 'haar')
    LL, (LH, HL, HH) = coeffs2

    flat_LL = LL.flatten()
    for i, bit in enumerate(message_bin):
        flat_LL[i] = flat_LL[i] + 1 if int(bit) == 1 else flat_LL[i]

    new_LL = flat_LL.reshape(LL.shape)
    new_coeffs2 = (new_LL, (LH, HL, HH))
    reconstructed_image = pywt.idwt2(new_coeffs2, 'haar')
    reconstructed_image = np.clip(reconstructed_image, 0, 255).astype(np.uint8)

    cv2.imwrite(output_path, reconstructed_image)
    print("Сообщение скрыто методом DWT и сохранено в:", output_path)


def extract_message_dwt(image_path):
    """
    Извлечение сообщения с использованием DWT.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Ошибка: не удалось загрузить изображение.")
        return

    coeffs2 = pywt.dwt2(image, 'haar')
    LL, (_, _, _) = coeffs2

    flat_LL = LL.flatten()
    binary_message = [str(int(value % 2)) for value in flat_LL]
    message_bin = ''.join(binary_message)
    extracted_message = ''
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i+8]
        if byte == '00000000':
            break
        extracted_message += chr(int(byte, 2))
    return extracted_message


if __name__ == "__main__":
    print("--- Многометодная стеганография ---")
    while True:
        print("\nВыберите метод и действие:")
        print("1. Скрыть сообщение (LSB)")
        print("2. Извлечь сообщение (LSB)")
        print("3. Скрыть сообщение (DWT)")
        print("4. Извлечь сообщение (DWT)")
        print("5. Выйти")
        choice = input("Ваш выбор: ")

        if choice == "1":
            image_path = input("Введите путь к изображению: ")
            message = input("Введите сообщение для скрытия: ")
            output_path = input("Введите путь для сохранения изображения: ")
            embed_message_lsb(image_path, message, output_path)
        elif choice == "2":
            image_path = input("Введите путь к изображению: ")
            print("Извлеченное сообщение (LSB):", extract_message_lsb(image_path))
        elif choice == "3":
            image_path = input("Введите путь к изображению: ")
            message = input("Введите сообщение для скрытия: ")
            output_path = input("Введите путь для сохранения изображения: ")
            embed_message_dwt(image_path, message, output_path)
        elif choice == "4":
            image_path = input("Введите путь к изображению: ")
            print("Извлеченное сообщение (DWT):", extract_message_dwt(image_path))
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
