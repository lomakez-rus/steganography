
# 🔒 Скрытие информации в изображениях и музыкальных файлах

Этот репозиторий содержит два инструмента для работы со стеганографией, позволяющих скрывать и извлекать текстовую информацию из изображений и аудиофайлов. Проект ориентирован на демонстрацию различных методов стеганографии, от простых до сложных.

# Проект создан следующими авторами:

Кульчинский Арсений

Чеб Артём

---

# 1. 🎵 MP3 Стеганография (простые методы)

## Описание
Этот Python-проект предоставляет функциональность для скрытия и извлечения информации из MP3-файлов с использованием различных методов стеганографии. Программа поддерживает шифрование для безопасного хранения сообщений и предлагает простое текстовое меню для взаимодействия.

Файл: mp3_steganography.py

---

## Возможности

1. **Методы скрытия сообщений:**
   - В метаданных MP3.
   - В конце MP3-файла.
   - С использованием шифрования для безопасного хранения.
   - В области выравнивания MP3-файла.
   - С использованием пользовательских маркеров (начальный и конечный теги).

2. **Методы извлечения сообщений:**
   - Из метаданных MP3.
   - Из конца MP3-файла.
   - Из зашифрованных данных.
   - Из области выравнивания.
   - С использованием пользовательских маркеров.

3. **Шифрование:**
   - Использует библиотеку `cryptography` для безопасного шифрования и дешифрования сообщений.

4. **Удобный интерфейс:**
   - Текстовое меню позволяет легко выбрать нужную опцию.

---


# 2. 🎵 MP3 Стеганография (сложные методы)

Файл: steganography_mp3_metods.py

MP3 Steganography Toolkit позволяет встраивать и извлекать скрытые сообщения в MP3-файлах с использованием сложных методов обработки аудиосигналов. Программа включает текстовое меню и поддерживает 5 методов стеганографии.

---

## 🔧 Функциональность

- **LSB (Least Significant Bit)**  
  Встраивание данных в младшие биты амплитуды звукового сигнала.
  
- **FFT (Fast Fourier Transform)**  
  Использует преобразование Фурье для внедрения данных в частотные компоненты аудиофайла.
  
- **DWT (Discrete Wavelet Transform)**  
  Делит сигнал на субдиапазоны и внедряет сообщение в низкочастотные компоненты.
  
- **DCT (Discrete Cosine Transform)**  
  Преобразование косинусов, используемое для скрытия данных в частотных коэффициентах.
  
- **Рандомизированный метод**  
  Встраивание данных с использованием случайного выбора точек в сигнале.

---


# 3. Стеганография с использованием DWT и QIM (для изображений)

Этот проект демонстрирует скрытие и извлечение текста в изображении с использованием **дискретного волнового преобразования (DWT)** и метода **квантования коэффициентов (QIM)**.

Файл: steganography_dwt_qim.py

## Особенности
- Используется низкочастотный диапазон (LL) изображения после преобразования DWT.
- Квантование коэффициентов LL для встраивания сообщений.
- Сообщение кодируется в двоичном формате с использованием шага квантования `delta`.

## Зависимости
Для работы программы требуются следующие библиотеки:
- Python 3.7+
- OpenCV
- NumPy
- PyWavelets

Установите зависимости с помощью:
```bash
pip install opencv-python-headless numpy pywavelets

```

---

# 4. Стеганография для PNG-изображений

Файл: steganography_methods.py

Этот проект содержит реализацию двух методов стеганографии для скрытия текста в PNG-изображениях: **LSB (Least Significant Bit)** и **DWT (Discrete Wavelet Transform)**.

## Методы

### 1. LSB (Младший значащий бит)
- **Описание**: Каждый байт пикселя изменяется, чтобы хранить один бит сообщения.
- **Преимущества**: Простота реализации.
- **Недостатки**: Уязвимость к любым изменениям изображения.
- **Использование**:
  - Скрытие: `embed_message_lsb(image_path, message, output_path)`
  - Извлечение: `extract_message_lsb(image_path)`

### 2. DWT (Дискретное волновое преобразование)
- **Описание**: Сообщение скрывается в низкочастотных коэффициентах изображения после преобразования DWT.
- **Преимущества**: Устойчивость к сжатию и фильтрации.
- **Недостатки**: Сложность реализации.
- **Использование**:
  - Скрытие: `embed_message_dwt(image_path, message, output_path)`
  - Извлечение: `extract_message_dwt(image_path)`

## Зависимости
- Python 3.7+
- OpenCV
- NumPy
- PyWavelets

Установите зависимости:
```bash
pip install opencv-python-headless numpy pywavelets

```

---

# 5. Стеганографии в JPG-изображениях

Файл: steganography_jpg.py

## Описание
Программа для стеганографии в JPG-изображениях. Реализовано 5 методов для скрытия информации:  
1. **LSB (Least Significant Bit)** – Изменение младших битов пикселей.  
2. **DCT (Discrete Cosine Transform)** – Встраивание в коэффициенты косинусного преобразования.  
3. **DWT (Discrete Wavelet Transform)** – Использование вейвлет-преобразования для скрытия данных.  
4. **FFT (Fast Fourier Transform)** – Манипуляция частотными компонентами изображения.  
5. **Рандомизированный метод** – Использование случайно выбранных пикселей для встраивания данных.

---

## Установка
1. Убедитесь, что у вас установлен Python 3.9+.
2. Установите зависимости:
   ```bash
   pip install numpy opencv-python pywavelets scipy

   ```


   # 6. 🖼️ Стеганография в PNG: Скрытие информации в различных каналах

   Файл: steganography_png.py

Этот проект реализует скрытие и извлечение текста в PNG-изображениях с использованием различных каналов. Программа предоставляет текстовое меню для выбора методов работы.

---

## 📋 Возможности программы

Программа поддерживает следующие функции:

1. **Скрытие текста в младших битах (LSB)**  
   - Текст записывается в младшие биты всех каналов RGB.
2. **Скрытие текста в красном канале (Red Channel)**  
   - Текст записывается только в красный канал изображения.
3. **Скрытие текста в зелёном канале (Green Channel)**  
   - Текст записывается только в зелёный канал изображения.
4. **Скрытие текста в синем канале (Blue Channel)**  
   - Текст записывается только в синий канал изображения.
5. **Скрытие текста в альфа-канале (Alpha Channel)**  
   - Текст записывается в альфа-канал (если присутствует).
6. **Извлечение текста (LSB)**  
   - Извлечение скрытого текста из младших бит изображения.

---

## 🛠️ Установка

1. Убедитесь, что у вас установлен Python (рекомендуется версия 3.7 или выше).
2. Установите библиотеку Pillow:
   ```bash
   pip install pillow

     ```

  # 7. 🖼️ Стеганография в PNG: Скрытие информации в различных каналах

Файл: Steganography_DCT_&_DWT.py

🔒 **Сложная стеганография для изображений на Python**  

Этот проект реализует **два сложных метода** стеганографии для скрытия текстовой информации в изображениях:

1. **DCT (дискретное косинусное преобразование)**  
   - Сообщение встраивается в **средне- и высокочастотные коэффициенты** DCT.  
   - Метод похож на сжатие JPEG, изменения незаметны для глаза.
   
2. **DWT (дискретное вейвлет-преобразование)**  
   - Использует вейвлет-преобразование **Haar** для скрытия данных.  
   - Сообщение записывается в **высокочастотные коэффициенты**.  

Программа работает в текстовом меню и позволяет **скрывать и извлекать** информацию.

---

## 🚀 **Установка**  
### **1. Установите зависимости**  
Перед запуском убедитесь, что у вас установлен Python **3.8+**.  
Установите необходимые библиотеки:  
```sh
pip install opencv-python numpy scipy pywavelets
```

### **2. Скачайте код**  
```sh
git clone https://github.com/username/steganography-dct-dwt.git
cd steganography-dct-dwt
```

---

## 🛠 **Как использовать**  
### **Запуск программы**  
```sh
python steganography.py
```

### **Меню**  
🔹 **1. Встроить сообщение (DCT)** — скрытие текста в изображении через DCT.  
🔹 **2. Извлечь сообщение (DCT)** — достать скрытый текст.  
🔹 **3. Встроить сообщение (DWT)** — скрытие через вейвлеты.  
🔹 **4. Извлечь сообщение (DWT)** — декодирование.  
🔹 **5. Выход**  

---

## 📌 **Примеры использования**  
### **Скрытие сообщения (DCT)**  
```sh
Введите путь к изображению: image.png  
Введите сообщение для скрытия: Секретный код 1234  
Введите имя выходного файла: stego_image.png  
[DCT] Сообщение встроено в stego_image.png
```

### **Извлечение (DCT)**  
```sh
Введите путь к изображению: stego_image.png  
Извлечённое сообщение (DCT): Секретный код 1234
```

### **Скрытие сообщения (DWT)**  
```sh
Введите путь к изображению: image.png  
Введите сообщение для скрытия: Важная информация  
Введите имя выходного файла: stego_dwt.png  
[DWT] Сообщение встроено в stego_dwt.png
```

### **Извлечение (DWT)**  
```sh
Введите путь к изображению: stego_dwt.png  
Извлечённое сообщение (DWT): Важная информация
```

---

## 📎 **Как это работает?**  
🟢 **DCT-метод:**  
- Разделяет изображение на блоки **8×8 пикселей**.  
- Применяет **дискретное косинусное преобразование (DCT)**.  
- Встраивает бит в коэффициент [1,2] блока.  

🟠 **DWT-метод:**  
- Разбивает изображение на частотные компоненты **(LL, LH, HL, HH)**.  
- Встраивает данные в **LH-компоненту (высокие частоты)**.  
- Обратное DWT восстанавливает изображение.  

Оба метода дают **высокую скрытность** и **устойчивость** к простым методам анализа.  
