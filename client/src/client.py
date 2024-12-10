import requests
import easygui
import os

server_ip_port = "127.0.0.1:8000"


def recognise_photo():
    try:
        url = f"http://{server_ip_port}/recognise"
        file_path = easygui.fileopenbox(filetypes=["*.docx"])
        # Открываем файл для чтения в бинарном режиме
        with open(file_path, 'rb') as file:
            # Создаем словарь с файлом для параметра 'files'
            files = {'file': file}
            # Делаем POST запрос, передавая 'files'
            response = requests.post(url, files=files)

        # Проверяем статус код ответа
        # response.raise_for_status()
        if response.status_code == 200:
            print("Файл успешно загружен.")
            print(response.json())  # Вывод ответа сервера
        else:
            print(f"Ошибка загрузки файла: {response.status_code}")
    except:
        pass


def get_file_table(filename):
    try:
        url = f"http://{server_ip_port}/get_file/{filename}"  # Замените на ваш URL
        # Делаем GET запрос
        response = requests.get(url)

        # Проверяем статус код ответа
        if response.status_code == 200:
            # Сохраняем содержимое файла
            with open(f"../client_data/{filename}", 'wb') as f:
                f.write(response.content)

            print(f"Файл {filename} успешно скачан.")
        else:
            print(f"Ошибка скачивания файла: {response.status_code}")
    except:
        pass


def upload_file_table():
    try:
        url = f"http://{server_ip_port}/upload"
        file_path = easygui.fileopenbox(filetypes=["*.docx"])
        # Открываем файл для чтения в бинарном режиме
        with open(file_path, 'rb') as file:
            # Создаем словарь с файлом для параметра 'files'
            files = {'file': file}
            # Делаем POST запрос, передавая 'files'
            response = requests.post(url, files=files)

        if response.status_code == 200:
            print("Файл успешно загружен.")
            print(response.json())  # Вывод ответа сервера
        else:
            print(f"Ошибка загрузки файла: {response.status_code}")
    except:
        pass


def start_excel():
    os.system('start excel.exe ../client_data/table.xlsx')
