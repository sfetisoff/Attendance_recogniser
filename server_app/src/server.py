import Recogniser
import Table
import pandas as pd


from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()


@app.post("/recognise")
async def recognise_file(file: UploadFile = File(...)):
    """
    Принимает фото, загружает на сервер, распознаёт его, загружает файл с таблицей в папку /tables
    """
    file_path = f"../server_img/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    path_to_image = f"../server_img/{file.filename}"
    recogniser = Recogniser.Recogniser(path_to_image)
    recogniser.rects_recognition_with_storage_steps()
    recogniser.col_and_rows()
    recogniser.crop_image_to_cells_with_storage()
    # print(recogniser.row_cnt,recogniser.col_cnt)
    recogniser.text_recognition_from_cells()
    SUPER_ARRAY = recogniser.get_text()
    a = Table.Table(recogniser.row_cnt, recogniser.col_cnt)
    a.text_array = SUPER_ARRAY
    a.fill_table()
    a.correct_table()
    #a.print_table()
    my_list = pd.DataFrame(a.get_table())
    path_to_file = '../server_data/table.xlsx'
    my_list.to_excel(path_to_file, sheet_name='students', index=False, header=False)
    return {"filepath": path_to_file}



@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Принимает файл, сохраняет его на сервере и возвращает информацию о файле.
    """
    file_path = f"../server_data/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"filename": file.filename, "filepath": file_path}

@app.get("/get_file/{filename}")
async def get_file(filename: str):
    """
    Возвращает файл по имени.
    """
    file_path = f"../server_data/{filename}"
    return FileResponse(file_path)