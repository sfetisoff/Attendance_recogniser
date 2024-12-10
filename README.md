# Schedule Recogniser


## Description
This application is designed to recognize the photo of the student attendance list and record it in the Excel file. This is a client-server architecture project. All calculations take place on the server, the client receives only the result, which can be edited and sent to the server for permanent storage.

## Screenshots
![MainWindow](https://gitlab.mai.ru/DAKudryashev/auroracvproject/-/blob/main/Main_window.jpg)
## Client-Server architecture
In this project, the server is created on the same machine as the client, if desired, you can run the server on another machine, for this the following files will need to be on the server:  
![server_files](https://gitlab.mai.ru/DAKudryashev/auroracvproject/-/blob/main/server_files.jpg)  
Next, you will have to specify a global ip server instead of the standard ip server

## Installation
It is necessary to install:  
-Pycharm with python 3.10+  
-TesseractOCR (link for install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki)  
-Microsoft Excel  

Next, in the initial Pycharm window, select 'get from VCS' and download this project.  
To install dependencies in cmd inside Pycharm from the project folder, you need to write:  
```pip install -r requirements.txt```  

To start the server, write in cmd inside Pycharm from the project folder:  
```uvicorn server:app --reload```  
Next, run the file main.py

In order for the recognition to work correctly, you need to add the names of those who may be in the group list to the file surnames.txt . This file is used to clean up the garbage that appears due to the inaccurate operation of Tesseract during recognition.  
![surnames](https://gitlab.mai.ru/DAKudryashev/auroracvproject/-/blob/main/surnames.jpg)  

## Usage
-Clicking on the "Распознать"(Recognize) button:   
Windows Explorer opens, select the image(file.jpg)(The examples are in the folder /image/example.jpg) that you want to recognize.   
It is important that it be evenly illuminated, there were no unnecessary objects in the picture, and the text of the students surnames was printed.

-Clicking on the "Результат"(Result) button:  
A file will be downloaded from the server table.xlsx.  
This file will be saved to a folder '/client_data/table.xlsx' and automatically open in Excel, where you can edit it and rename it if desired.


-Clicking on the "Загрузить на сервер"(Upload to server) button:  
Windows Explorer opens, select the file (file.xlsx), which you want to upload to the server for permanent storage.  
This file will be saved on the server in the folder '/server_data/file.xlsx'

## Support
If you do not download the file when you click the "Результат"(Result) or "Загрузить на сервер"(Upload to the server) buttons, try closing Excel,  because when when performing actions to upload/download Excel files, it must be closed.

This project works with Russian, but does not work with English. This can be fixed in the program code by replacing line 181 in the Recogniser file with the line  
```text = pytesseract.image_to_string(cropped_image, lang='eng', config=custom_config)```


## Authors and acknowledgment
DAKudryashev, SAFetisov

