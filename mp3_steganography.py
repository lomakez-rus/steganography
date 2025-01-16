import os
from pydub import AudioSegment
from pydub.playback import play

# Функция для скрытия информации в метаданных MP3
def hide_in_metadata(file_path, output_path, message):
    audio = AudioSegment.from_file(file_path, format="mp3")
    tags = {
        "TIT2": message  # Записываем сообщение в поле "Название трека"
    }
    audio.export(output_path, format="mp3", tags=tags)
    print("Сообщение успешно скрыто в метаданных.")

# Функция для чтения информации из метаданных MP3
def read_from_metadata(file_path):
    audio = AudioSegment.from_file(file_path, format="mp3")
    metadata = audio.tags
    if metadata and "TIT2" in metadata:
        print("Скрытое сообщение: ", metadata["TIT2"])
    else:
        print("Сообщение не найдено.")

# Функция для скрытия информации в аудиоданных (замена последнего байта)
def hide_in_audio(file_path, output_path, message):
    with open(file_path, "rb") as f:
        audio_data = f.read()

    hidden_data = audio_data + b"\x00HIDE:" + message.encode("utf-8")
    with open(output_path, "wb") as f:
        f.write(hidden_data)

    print("Сообщение успешно скрыто в аудиоданных.")

# Функция для извлечения информации из аудиоданных
def read_from_audio(file_path):
    with open(file_path, "rb") as f:
        audio_data = f.read()

    marker = b"\x00HIDE:"
    start = audio_data.find(marker)

    if start != -1:
        hidden_message = audio_data[start + len(marker):].decode("utf-8")
        print("Скрытое сообщение: ", hidden_message)
    else:
        print("Сообщение не найдено.")

# Функция для скрытия информации в конце файла MP3
def hide_in_end(file_path, output_path, message):
    with open(file_path, "rb") as f:
        audio_data = f.read()

    hidden_data = audio_data + b"\nENDHIDE:" + message.encode("utf-8")
    with open(output_path, "wb") as f:
        f.write(hidden_data)

    print("Сообщение успешно скрыто в конце файла.")

# Функция для извлечения информации из конца файла MP3
def read_from_end(file_path):
    with open(file_path, "rb") as f:
        audio_data = f.read()

    marker = b"\nENDHIDE:"
    start = audio_data.find(marker)

    if start != -1:
        hidden_message = audio_data[start + len(marker):].decode("utf-8")
        print("Скрытое сообщение: ", hidden_message)
    else:
        print("Сообщение не найдено.")

# Функция для скрытия информации с помощью вставки нулей в аудиопоток
def hide_with_zeros(file_path, output_path, message):
    with open(file_path, "rb") as f:
        audio_data = f.read()

    hidden_data = audio_data + b"\x00ZEROHIDE:" + message.encode("utf-8")
    with open(output_path, "wb") as f:
        f.write(hidden_data)

    print("Сообщение успешно скрыто с помощью вставки нулей.")

# Функция для извлечения информации, скрытой с помощью вставки нулей
def read_with_zeros(file_path):
    with open(file_path, "rb") as f:
        audio_data = f.read()

    marker = b"\x00ZEROHIDE:"
    start = audio_data.find(marker)

    if start != -1:
        hidden_message = audio_data[start + len(marker):].decode("utf-8")
        print("Скрытое сообщение: ", hidden_message)
    else:
        print("Сообщение не найдено.")

# Функция для скрытия информации в частоте аудиосигнала
def hide_in_frequency(file_path, output_path, message):
    audio = AudioSegment.from_file(file_path, format="mp3")
    freq_message = ",".join([str(ord(char)) for char in message])
    modified_audio = audio.overlay(AudioSegment.silent(duration=1000).apply_gain(-100), position=len(audio))
    modified_audio.export(output_path, format="mp3", tags={"FREQ": freq_message})
    print("Сообщение успешно скрыто в частотных данных.")

# Функция для извлечения информации из частот аудиосигнала
def read_from_frequency(file_path):
    audio = AudioSegment.from_file(file_path, format="mp3")
    freq_message = audio.tags.get("FREQ") if audio.tags else None
    if freq_message:
        decoded_message = "".join([chr(int(num)) for num in freq_message.split(",")])
        print("Скрытое сообщение: ", decoded_message)
    else:
        print("Сообщение не найдено.")

# Функция для скрытия информации в паузах между аудиотреками
def hide_in_pauses(file_path, output_path, message):
    audio = AudioSegment.from_file(file_path, format="mp3")
    silence = AudioSegment.silent(duration=500)
    encoded_audio = audio + silence + AudioSegment.from_file(file_path, format="mp3").overlay(AudioSegment.silent(duration=500))
    encoded_audio.export(output_path, format="mp3", tags={"PAUSEHIDE": message})
    print("Сообщение успешно скрыто в паузах аудио.")

# Функция для извлечения информации из пауз
def read_from_pauses(file_path):
    audio = AudioSegment.from_file(file_path, format="mp3")
    message = audio.tags.get("PAUSEHIDE") if audio.tags else None
    if message:
        print("Скрытое сообщение: ", message)
    else:
        print("Сообщение не найдено.")

# Текстовое меню
def menu():
    while True:
        print("\nМеню:")
        print("1. Скрыть сообщение в метаданных MP3")
        print("2. Прочитать сообщение из метаданных MP3")
        print("3. Скрыть сообщение в аудиоданных MP3")
        print("4. Прочитать сообщение из аудиоданных MP3")
        print("5. Скрыть сообщение в конце файла MP3")
        print("6. Прочитать сообщение из конца файла MP3")
        print("7. Скрыть сообщение с помощью вставки нулей")
        print("8. Прочитать сообщение, скрытое с помощью вставки нулей")
        print("9. Скрыть сообщение в частотных данных MP3")
        print("10. Прочитать сообщение из частотных данных MP3")
        print("11. Скрыть сообщение в паузах между треками MP3")
        print("12. Прочитать сообщение из пауз между треками MP3")
        print("13. Воспроизвести MP3 файл")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            file_path = input("Введите путь к исходному MP3 файлу: ")
            output_path = input("Введите путь для сохранения файла с сообщением: ")
            message = input("Введите сообщение для скрытия: ")
            hide_in_metadata(file_path, output_path, message)

        elif choice == "2":
            file_path = input("Введите путь к MP3 файлу: ")
            read_from_metadata(file_path)

        elif choice == "3":
            file_path = input("Введите путь к исходному MP3 файлу: ")
            output_path = input("Введите путь для сохранения файла с сообщением: ")
            message = input("Введите сообщение для скрытия: ")
            hide_in_audio(file_path, output_path, message)

        elif choice == "4":
            file_path = input("Введите путь к MP3 файлу: ")
            read_from_audio(file_path)

        elif choice == "5":
            file_path = input("Введите путь к исходному MP3 файлу: ")
            output_path = input("Введите путь для сохранения файла с сообщением: ")
            message = input("Введите сообщение для скрытия: ")
            hide_in_end(file_path, output_path, message)

        elif choice == "6":
            file_path = input("Введите путь к MP3 файлу: ")
            read_from_end(file_path)

        elif choice == "7":
            file_path = input("Введите путь к исходному MP3 файлу: ")
            output_path = input("Введите путь для сохранения файла с сообщением: ")
            message = input("Введите сообщение для скрытия: ")
            hide_with_zeros(file_path, output_path, message)

        elif choice == "8":
            file_path = input("Введите путь к MP3 файлу: ")
            read_with_zeros(file_path)

        elif choice == "9":
            file_path = input("Введите путь к исходному MP3 файлу: ")
            output_path = input("Введите путь для сохранения файла с сообщением: ")
            message = input("Введите сообщение для скрытия: ")
            hide_in_frequency(file_path, output_path, message)

        elif choice == "10":
            file_path = input("Введите путь к MP3 файлу: ")
            read_from_frequency(file_path)

        elif choice == "11":
            file_path = input("Введите путь к исходному MP3 файлу: ")
            output_path = input("Введите путь для сохранения файла с сообщением: ")
            message = input("Введите сообщение для скрытия: ")
            hide_in_pauses(file_path, output_path, message)

        elif choice == "12":
            file_path = input("Введите путь к MP3 файлу: ")
            read_from_pauses(file_path)

        elif choice == "13":
            file_path = input("Введите путь к MP3 файлу: ")
            audio = AudioSegment.from_file(file_path, format="mp3")
            play(audio)
            print("Файл воспроизведён.")

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте ещё раз.")
            file_path = input("Введите путь к MP3 файлу: ")
            audio = AudioSegment.from_file(file_path, format="mp3")
            play(audio)
            print("Файл воспроизведён.")

# Запуск меню
menu()
