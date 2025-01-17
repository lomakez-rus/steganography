import numpy as np
import cv2
import pywt
import random
import scipy.fftpack as fftpack


def menu():
    print("\nJPG Steganography Toolkit")
    print("1. LSB (Least Significant Bit)")
    print("2. DCT (Discrete Cosine Transform)")
    print("3. DWT (Discrete Wavelet Transform)")
    print("4. FFT (Fast Fourier Transform)")
    print("5. Рандомизированный метод")
    print("6. Выход")
    return input("Выберите метод: ")


def lsb_embed(image, message):
    binary_message = ''.join(format(ord(ch), '08b') for ch in message) + '1111111111111110'  # Сообщение + стоп-код
    flat_image = image.flatten()
    for i, bit in enumerate(binary_message):
        flat_image[i] = (flat_image[i] & ~1) | int(bit)
    return flat_image.reshape(image.shape)


def lsb_extract(image):
    flat_image = image.flatten()
    binary_message = ''.join(str(flat_image[i] & 1) for i in range(flat_image.size))
    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    return message.split('\x00')[0]  # Удаляем символы после стоп-кода


def dct_embed(image, message):
    binary_message = ''.join(format(ord(ch), '08b') for ch in message) + '1111111111111110'
    h, w, _ = image.shape
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    for i, bit in enumerate(binary_message):
        x, y = divmod(i, w)
        block = image[x:x+8, y:y+8, 0]
        dct_block = cv2.dct(block.astype(np.float32))
        dct_block[4, 4] = dct_block[4, 4] + (1 if bit == '1' else -1)
        image[x:x+8, y:y+8, 0] = cv2.idct(dct_block).astype(np.uint8)
    return cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)


def dct_extract(image):
    h, w, _ = image.shape
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    binary_message = ''
    for x in range(0, h, 8):
        for y in range(0, w, 8):
            block = image[x:x+8, y:y+8, 0]
            dct_block = cv2.dct(block.astype(np.float32))
            binary_message += '1' if dct_block[4, 4] > 0 else '0'
            if binary_message.endswith('1111111111111110'):
                break
    return ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))


def dwt_embed(image, message):
    coeffs2 = pywt.dwt2(image[:, :, 0], 'haar')
    LL, (LH, HL, HH) = coeffs2
    binary_message = ''.join(format(ord(ch), '08b') for ch in message) + '1111111111111110'
    for i, bit in enumerate(binary_message):
        LL.flat[i] = LL.flat[i] + (1 if bit == '1' else -1)
    coeffs2 = LL, (LH, HL, HH)
    image[:, :, 0] = pywt.idwt2(coeffs2, 'haar')
    return image


def dwt_extract(image):
    coeffs2 = pywt.dwt2(image[:, :, 0], 'haar')
    LL, _ = coeffs2
    binary_message = ''.join('1' if LL.flat[i] > 0 else '0' for i in range(LL.size))
    return ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))


def fft_embed(image, message):
    binary_message = ''.join(format(ord(ch), '08b') for ch in message) + '1111111111111110'
    fft_image = fftpack.fft2(image[:, :, 0])
    for i, bit in enumerate(binary_message):
        fft_image.flat[i] = fft_image.flat[i] + (1 if bit == '1' else -1)
    image[:, :, 0] = fftpack.ifft2(fft_image).real
    return image


def fft_extract(image):
    fft_image = fftpack.fft2(image[:, :, 0])
    binary_message = ''.join('1' if fft_image.flat[i] > 0 else '0' for i in range(fft_image.size))
    return ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))


def randomized_embed(image, message):
    random.seed(42)
    binary_message = ''.join(format(ord(ch), '08b') for ch in message) + '1111111111111110'
    indices = random.sample(range(image.size), len(binary_message))
    for i, bit in enumerate(binary_message):
        image.flat[indices[i]] = (image.flat[indices[i]] & ~1) | int(bit)
    return image


def randomized_extract(image):
    random.seed(42)
    indices = random.sample(range(image.size), 64)  # Длина должна быть заранее известна
    binary_message = ''.join(str(image.flat[i] & 1) for i in indices)
    return ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))


if __name__ == "__main__":
    while True:
        choice = menu()
        if choice == "1":
            print("LSB метод выбран.")
        elif choice == "6":
            break
