# Schedule Recogniser


## Description
This application is designed to recognize the photo of the student attendance list and record it in the Excel file. This is a client-server architecture project. All calculations take place on the server, the client receives only the result, which can be edited and sent to the server for permanent storage.

## Installation
The Excel must be present on the client's computer

To install dependencies for client in cmd inside Pycharm from the project folder, you need to write:  
```pip install -r ./client/requirements.txt```  

To start the server, write:  
``` docker run -d --name server-container -p 8000:8000/tcp sfetisoff/server-recogniser```

``-d`` means that container is running in detached mode

`-p 8000:8000/tcp` used to forward ports between the host and the container, allowing network traffic to be redirected from a port on the host to a port in the container

To start client app run client/main.py

In order for the recognition to work correctly, you need to add the names of those who may be in the group list to the file surnames.txt . This file is used to clean up the garbage that appears due to the inaccurate operation of Tesseract during recognition.

## Usage
-Clicking on the "Распознать"(Recognize) button:   
Windows Explorer opens, select the image(file.jpg)(The examples are in the folder /client/images/example.jpg) that you want to recognize.   
It is important that it be evenly illuminated, there were no unnecessary objects in the picture, and the text of the students surnames was printed.

-Clicking on the "Результат"(Result) button:  
A file will be downloaded from the server table.xlsx.  
This file will be saved to a folder '/client_data/table.xlsx' and automatically open in Excel, where you can edit it and rename it if desired.


-Clicking on the "Загрузить на сервер"(Upload to server) button:  
Windows Explorer opens, select the file (file.xlsx), which you want to upload to the server for permanent storage.  
This file will be saved on the server in the folder '/server_data/file.xlsx'

## Support
If you do not download the file when you click the "Результат"(Result) or "Загрузить на сервер"(Upload to the server) buttons, try closing Excel, because when when performing actions to upload/download Excel files, it must be closed.

This project works with Russian, but does not work with English. This can be fixed in the program code by replacing line 181 in the Recogniser file with the line  
```text = pytesseract.image_to_string(cropped_image, lang='eng', config=custom_config)```


## Authors and acknowledgment
DAKudryashev, sfetisoff

