import cv2
import numpy as np
import pywt


def embed_message_dwt_qim(image_path, message, output_path, delta=10):
    """
    Скрытие сообщения с использованием DWT и QIM.
    :param image_path: Путь к изображению.
    :param message: Сообщение для скрытия.
    :param output_path: Путь для сохранения изображения.
    :param delta: Шаг квантования (по умолчанию 10).
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Ошибка: не удалось загрузить изображение.")
        return

    message_bin = ''.join(format(ord(char), '08b') for char in message) + '00000000'

    coeffs2 = pywt.dwt2(image, 'haar')
    LL, (LH, HL, HH) = coeffs2

    flat_LL = LL.flatten()
    for i in range(len(message_bin)):
        bit = int(message_bin[i])
        quantized_value = delta * round(flat_LL[i] / delta)
        if bit == 1:
            if quantized_value % (2 * delta) == 0:
                flat_LL[i] = quantized_value + delta
            else:
                flat_LL[i] = quantized_value
        else:
            if quantized_value % (2 * delta) != 0:
                flat_LL[i] = quantized_value + delta
            else:
                flat_LL[i] = quantized_value

    new_LL = flat_LL.reshape(LL.shape)
    new_coeffs2 = (new_LL, (LH, HL, HH))
    reconstructed_image = pywt.idwt2(new_coeffs2, 'haar')
    reconstructed_image = np.clip(reconstructed_image, 0, 255).astype(np.uint8)

    cv2.imwrite(output_path, reconstructed_image)
    print("Сообщение скрыто и сохранено в:", output_path)


def extract_message_dwt_qim(image_path, delta=10):
    """
    Извлечение сообщения из изображения с использованием DWT и QIM.
    :param image_path: Путь к изображению.
    :param delta: Шаг квантования (по умолчанию 10).
    :return: Извлеченное сообщение.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Ошибка: не удалось загрузить изображение.")
        return

    coeffs2 = pywt.dwt2(image, 'haar')
    LL, (LH, HL, HH) = coeffs2

    flat_LL = LL.flatten()
    binary_message = []
    for value in flat_LL:
        if value % (2 * delta) == 0:
            binary_message.append('0')
        else:
            binary_message.append('1')

    binary_message = ''.join(binary_message)
    extracted_message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '00000000':
            break
        extracted_message += chr(int(byte, 2))
    return extracted_message


if __name__ == "__main__":
    print("--- Сложная стеганография: DWT + QIM ---")
    while True:
        print("\nВыберите действие:")
        print("1. Скрыть сообщение")
        print("2. Раскрыть сообщение")
        print("3. Выйти")
        choice = input("Ваш выбор: ")

        if choice == "1":
            image_path = input("Введите путь к изображению: ")
            message = input("Введите сообщение для скрытия: ")
            output_path = input("Введите путь для сохранения изображения: ")
            embed_message_dwt_qim(image_path, message, output_path)
        elif choice == "2":
            image_path = input("Введите путь к изображению: ")
            print("Извлеченное сообщение:", extract_message_dwt_qim(image_path))
        elif choice == "3":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
