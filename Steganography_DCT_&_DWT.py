import cv2
import numpy as np
import scipy.fftpack
import pywt

def embed_message_dct(image_path, message, output_path):
    """Внедряет сообщение в изображение с использованием DCT."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape

    message_bin = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'
    msg_index = 0

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            if msg_index >= len(message_bin):
                break

            block = np.float32(img[i:i+8, j:j+8]) - 128
            dct_block = scipy.fftpack.dct(scipy.fftpack.dct(block.T, norm='ortho').T, norm='ortho')

            if message_bin[msg_index] == '1':
                dct_block[1, 2] += 5
            else:
                dct_block[1, 2] -= 5

            msg_index += 1
            
            idct_block = scipy.fftpack.idct(scipy.fftpack.idct(dct_block.T, norm='ortho').T, norm='ortho')
            img[i:i+8, j:j+8] = np.clip(idct_block + 128, 0, 255)

    cv2.imwrite(output_path, img)
    print(f"[DCT] Сообщение встроено в {output_path}")

def extract_message_dct(image_path):
    """Извлекает скрытое сообщение из изображения с использованием DCT."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    message_bin = ""

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            block = np.float32(img[i:i+8, j:j+8]) - 128
            dct_block = scipy.fftpack.dct(scipy.fftpack.dct(block.T, norm='ortho').T, norm='ortho')

            bit = '1' if dct_block[1, 2] > 0 else '0'
            message_bin += bit

            if message_bin.endswith('1111111111111110'):
                break

    message_bin = message_bin[:-16]
    message = ''.join(chr(int(message_bin[i:i+8], 2)) for i in range(0, len(message_bin), 8))
    return message

def embed_message_dwt(image_path, message, output_path):
    """Внедряет сообщение в изображение с использованием DWT."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)
    
    # Выполняем одноуровневое дискретное вейвлет-преобразование (DWT)
    coeffs2 = pywt.dwt2(img, 'haar')
    LL, (LH, HL, HH) = coeffs2
    
    message_bin = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'
    msg_index = 0

    h, w = LH.shape
    for i in range(h):
        for j in range(w):
            if msg_index >= len(message_bin):
                break
            LH[i, j] = LH[i, j] + 0.5 if message_bin[msg_index] == '1' else LH[i, j] - 0.5
            msg_index += 1

    # Выполняем обратное DWT
    img_stego = pywt.idwt2((LL, (LH, HL, HH)), 'haar')
    img_stego = np.clip(img_stego, 0, 255).astype(np.uint8)
    
    cv2.imwrite(output_path, img_stego)
    print(f"[DWT] Сообщение встроено в {output_path}")

def extract_message_dwt(image_path):
    """Извлекает скрытое сообщение из изображения с использованием DWT."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)
    coeffs2 = pywt.dwt2(img, 'haar')
    _, (LH, _, _) = coeffs2
    
    message_bin = ""
    h, w = LH.shape

    for i in range(h):
        for j in range(w):
            bit = '1' if LH[i, j] > 0 else '0'
            message_bin += bit
            if message_bin.endswith('1111111111111110'):
                break

    message_bin = message_bin[:-16]
    message = ''.join(chr(int(message_bin[i:i+8], 2)) for i in range(0, len(message_bin), 8))
    return message

def menu():
    """Текстовое меню для выбора метода стеганографии."""
    while True:
        print("\nСтеганография (DCT и DWT)")
        print("1. Встроить сообщение (DCT)")
        print("2. Извлечь сообщение (DCT)")
        print("3. Встроить сообщение (DWT)")
        print("4. Извлечь сообщение (DWT)")
        print("5. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            image_path = input("Введите путь к изображению: ")
            message = input("Введите сообщение для скрытия: ")
            output_path = input("Введите имя выходного файла: ")
            embed_message_dct(image_path, message, output_path)

        elif choice == '2':
            image_path = input("Введите путь к изображению со скрытым сообщением: ")
            extracted_message = extract_message_dct(image_path)
            print("Извлечённое сообщение (DCT):", extracted_message)

        elif choice == '3':
            image_path = input("Введите путь к изображению: ")
            message = input("Введите сообщение для скрытия: ")
            output_path = input("Введите имя выходного файла: ")
            embed_message_dwt(image_path, message, output_path)

        elif choice == '4':
            image_path = input("Введите путь к изображению со скрытым сообщением: ")
            extracted_message = extract_message_dwt(image_path)
            print("Извлечённое сообщение (DWT):", extracted_message)

        elif choice == '5':
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод, попробуйте снова.")

if __name__ == "__main__":
    menu()
