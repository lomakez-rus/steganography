import numpy as np
from pydub import AudioSegment
from scipy.fftpack import fft, ifft
import pywt
import random


def menu():
    print("\nMP3 Steganography Toolkit")
    print("1. LSB (Least Significant Bit)")
    print("2. FFT (Fast Fourier Transform)")
    print("3. DCT (Discrete Cosine Transform)")
    print("4. DWT (Discrete Wavelet Transform)")
    print("5. Рандомизированный метод")
    print("6. Выход")
    return input("Выберите метод: ")


def load_audio(file_path):
    audio = AudioSegment.from_mp3(file_path)
    samples = np.array(audio.get_array_of_samples())
    return audio, samples


def save_audio(audio, samples, output_file):
    samples = samples.astype(np.int16)
    modified_audio = audio._spawn(samples.tobytes())
    modified_audio.export(output_file, format="mp3")


def lsb_embed(samples, message):
    binary_message = ''.join(format(ord(ch), '08b') for ch in message) + '1111111111111110'
    for i, bit in enumerate(binary_message):
        samples[i] = (samples[i] & ~1) | int(bit)
    return samples


def lsb_extract(samples):
    binary_message = ''.join(str(samples[i] & 1) for i in range(len(samples)))
    chars = [chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8)]
    return ''.join(chars).split('\x00')[0]


def fft_embed(samples, message):
    binary_message = ''.join(format(ord(ch), '08b') for ch in message) + '1111111111111110'
    freq_domain = fft(samples)
    for i, bit in enumerate(binary_message):
        freq_domain[i] += (1 if bit == '1' else -1)
    return np.real(ifft(freq_domain)).astype(np.int16)


def fft_extract(samples):
    freq_domain = fft(samples)
    binary_message = ''.join('1' if freq_domain[i].real > 0 else '0' for i in range(len(freq_domain)))
    chars = [chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8)]
    return ''.join(chars).split('\x00')[0]


def dwt_embed(samples, message):
    coeffs = pywt.wavedec(samples, 'haar', level=2)
    binary_message = ''.join(format(ord(ch), '08b') for ch in message) + '1111111111111110'
    LL = coeffs[0]
    for i, bit in enumerate(binary_message):
        LL[i] += (1 if bit == '1' else -1)
    coeffs[0] = LL
    return pywt.waverec(coeffs, 'haar').astype(np.int16)


def dwt_extract(samples):
    coeffs = pywt.wavedec(samples, 'haar', level=2)
    LL = coeffs[0]
    binary_message = ''.join('1' if LL[i] > 0 else '0' for i in range(len(LL)))
    chars = [chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8)]
    return ''.join(chars).split('\x00')[0]


def randomized_embed(samples, message):
    random.seed(42)
    binary_message = ''.join(format(ord(ch), '08b') for ch in message) + '1111111111111110'
    indices = random.sample(range(len(samples)), len(binary_message))
    for i, bit in enumerate(binary_message):
        samples[indices[i]] = (samples[indices[i]] & ~1) | int(bit)
    return samples


def randomized_extract(samples):
    random.seed(42)
    indices = random.sample(range(len(samples)), 64)  # Предполагаемая длина сообщения
    binary_message = ''.join(str(samples[i] & 1) for i in indices)
    chars = [chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8)]
    return ''.join(chars).split('\x00')[0]


if __name__ == "__main__":
    while True:
        choice = menu()
        if choice == "1":
            print("LSB метод выбран.")
            input_file = input("Введите путь к MP3-файлу: ")
            message = input("Введите сообщение: ")
            output_file = input("Введите имя выходного файла: ")
            audio, samples = load_audio(input_file)
            modified_samples = lsb_embed(samples, message)
            save_audio(audio, modified_samples, output_file)
            print(f"Сообщение встроено в файл {output_file}.")
        elif choice == "2":
            print("FFT метод выбран.")
            input_file = input("Введите путь к MP3-файлу: ")
            message = input("Введите сообщение: ")
            output_file = input("Введите имя выходного файла: ")
            audio, samples = load_audio(input_file)
            modified_samples = fft_embed(samples, message)
            save_audio(audio, modified_samples, output_file)
            print(f"Сообщение встроено в файл {output_file}.")
        elif choice == "6":
            print("Выход.")
            break
        else:
            print("Метод еще не реализован.")
