import cv2
import numpy as np
from pydub import AudioSegment
import wave
import pywt
import random

def encode_lsb(image_path, message, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    message += "#####"
    message_bin = ''.join(format(ord(i), '08b') for i in message)
    
    rows, cols, _ = img.shape
    index = 0
    
    for i in range(rows):
        for j in range(cols):
            if index < len(message_bin):
                for k in range(3):
                    if index < len(message_bin):
                        img[i, j, k] = int(format(img[i, j, k], '08b')[:-1] + message_bin[index], 2)
                        index += 1
    cv2.imwrite(output_path, img)

def decode_lsb(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    message_bin = ""
    
    rows, cols, _ = img.shape
    for i in range(rows):
        for j in range(cols):
            for k in range(3):
                message_bin += str(img[i, j, k] & 1)
    
    message = ""
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i+8]
        character = chr(int(byte, 2))
        message += character
        if message.endswith("#####"):
            break
    
    return message[:-5]

def encode_dct(image_path, message, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    message += "#####"
    message_bin = ''.join(format(ord(i), '08b') for i in message)
    
    rows, cols, _ = img.shape
    index = 0
    
    for i in range(rows):
        for j in range(cols):
            if index < len(message_bin):
                for k in range(3):
                    if index < len(message_bin):
                        img[i, j, k] = int(format(img[i, j, k], '08b')[:-1] + message_bin[index], 2)
                        index += 1
    cv2.imwrite(output_path, img)

def decode_dct(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    message_bin = ""
    
    rows, cols, _ = img.shape
    for i in range(rows):
        for j in range(cols):
            for k in range(3):
                message_bin += str(img[i, j, k] & 1)
    
    message = ""
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i+8]
        character = chr(int(byte, 2))
        message += character
        if message.endswith("#####"):
            break
    
    return message[:-5]

def encode_dwt(image_path, message, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    message += "#####"
    message_bin = ''.join(format(ord(i), '08b') for i in message)
    
    coeffs = pywt.dwt2(img, 'haar')
    LL, (LH, HL, HH) = coeffs
    
    index = 0
    for i in range(LL.shape[0]):
        for j in range(LL.shape[1]):
            if index < len(message_bin):
                LL[i, j] = int(LL[i, j]) & ~1 | int(message_bin[index])
                index += 1
    
    img_encoded = pywt.idwt2((LL, (LH, HL, HH)), 'haar')
    img_encoded = np.uint8(img_encoded)
    cv2.imwrite(output_path, img_encoded)

def decode_dwt(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    coeffs = pywt.dwt2(img, 'haar')
    LL, (LH, HL, HH) = coeffs
    
    message_bin = ""
    for i in range(LL.shape[0]):
        for j in range(LL.shape[1]):
            message_bin += str(int(LL[i, j]) & 1)
    
    message = ""
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i+8]
        character = chr(int(byte, 2))
        message += character
        if message.endswith("#####"):
            break
    
    return message[:-5]

def encode_fft(image_path, message, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    message += "#####"
    message_bin = ''.join(format(ord(i), '08b') for i in message)
    
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    
    rows, cols = magnitude_spectrum.shape
    index = 0
    for i in range(rows):
        for j in range(cols):
            if index < len(message_bin):
                magnitude_spectrum[i, j] = int(magnitude_spectrum[i, j]) & ~1 | int(message_bin[index])
                index += 1
    
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    cv2.imwrite(output_path, img_back)

def decode_fft(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    
    message_bin = ""
    rows, cols = magnitude_spectrum.shape
    for i in range(rows):
        for j in range(cols):
            message_bin += str(int(magnitude_spectrum[i, j]) & 1)
    
    message = ""
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i+8]
        character = chr(int(byte, 2))
        message += character
        if message.endswith("#####"):
            break
    
    return message[:-5]

def encode_random(image_path, message, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    message += "#####"
    message_bin = ''.join(format(ord(i), '08b') for i in message)
    
    rows, cols, _ = img.shape
    indices = list(range(rows * cols * 3))
    random.shuffle(indices)
    
    index = 0
    for idx in indices:
        if index < len(message_bin):
            row = idx // (cols * 3)
            col = (idx % (cols * 3)) // 3
            channel = idx % 3
            img[row, col, channel] = int(format(img[row, col, channel], '08b')[:-1] + message_bin[index], 2)
            index += 1
    cv2.imwrite(output_path, img)

def decode_random(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    message_bin = ""
    
    rows, cols, _ = img.shape
    indices = list(range(rows * cols * 3))
    random.shuffle(indices)
    
    for idx in indices:
        row = idx // (cols * 3)
        col = (idx % (cols * 3)) // 3
        channel = idx % 3
        message_bin += str(img[row, col, channel] & 1)
    
    message = ""
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i+8]
        character = chr(int(byte, 2))
        message += character
        if message.endswith("#####"):
            break
    
    return message[:-5]

def main():
    while True:
        print("Выберите метод стеганографии:")
        print("1. LSB (Least Significant Bit)")
        print("2. DCT (Discrete Cosine Transform)")
        print("3. DWT (Discrete Wavelet Transform)")
        print("4. FFT (Fast Fourier Transform)")
        print("5. Рандомизированный метод")
        print("6. Выход")
        
        choice = int(input("Введите номер метода: "))
        
        if choice == 6:
            break
        
        action = input("Выберите действие (encode/decode): ")
        image_path = input("Введите путь к изображению: ")
        
        if action == "encode":
            message = input("Введите сообщение для скрытия: ")
            output_path = input("Введите путь для сохранения скрытого изображения: ")
            
            if choice == 1:
                encode_lsb(image_path, message, output_path)
            elif choice == 2:
                encode_dct(image_path, message, output_path)
            elif choice == 3:
                encode_dwt(image_path, message, output_path)
            elif choice == 4:
                encode_fft(image_path, message, output_path)
            elif choice == 5:
                encode_random(image_path, message, output_path)
            else:
                print("Неверный выбор, попробуйте еще раз.")
        
        elif action == "decode":
            if choice == 1:
                print("Скрытое сообщение:", decode_lsb(image_path))
            elif choice == 2:
                                print("Скрытое сообщение:", decode_dct(image_path))
            elif choice == 3:
                print("Скрытое сообщение:", decode_dwt(image_path))
            elif choice == 4:
                print("Скрытое сообщение:", decode_fft(image_path))
            elif choice == 5:
                print("Скрытое сообщение:", decode_random(image_path))
            else:
                print("Неверный выбор, попробуйте еще раз.")
        else:
            print("Неверное действие, попробуйте еще раз.")

if __name__ == "__main__":
    main()
