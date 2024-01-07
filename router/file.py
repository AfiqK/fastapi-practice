import shutil
import pytesseract
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse


router = APIRouter(
    prefix = '/title',
    tags=['file']
)

@router.post('/file')
def get_file(file: bytes = File()):
    content = file.decode('utf-8')
    lines = content.split('\r\n')
    return {'lines': lines}

@router.post('/ocr')
def get_ocr(upload_file: UploadFile):
    path = f"files/{upload_file.filename}"
    with open (path, "w+b") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return pytesseract.image_to_string(path, lang='eng')

@router.post('uploadfile')
def get_uploadfile(upload_file: UploadFile = File()):
    path = f"files/{upload_file.filename}"
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return{
        'filename': path,
        'type': upload_file.content_type
    }

@router.get('/download/{name}', response_class=FileResponse)
def get_file(name: str):
    path = f"files/{name}"
    return path